import os
import asyncio
import hashlib
import json
from uuid import uuid4
import cv2
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from neo4j import AsyncSession
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_neo4j_session, get_postgres_db
from app.helper.minio_helper import sync_minio_upload
from app.minio import minio_client
from app.model.student import Student
from app.schemas.management_schemas import ExtractStudentActivitiesResponse, ExtractStudentDescriptionResponse, ExtractStudentFromFrameResponse
from app.yolo_behaviour_detection import detect_behaviour
from app.yolo_face_dectection import detect_face
from app.helper.yolo_helper import convert_yolo_result, match_behaviour_with_face

extract = APIRouter(prefix="/extract", tags= ["ExtractYolo"])

# Initialize the LLM (Use gpt-4o or similar for high accuracy in Cypher)
llm = ChatOpenAI(model="gpt-5-nano", temperature=0, api_key= os.getenv("OPENAI_API_KEY"),)

template = """
You are a data assistant. Use the following JSON data to answer the user's question.
If the answer isn't in the data, honestly say you don't know.

DATA:
{json_data}

USER QUESTION: 
{user_question}
"""

prompt_template = ChatPromptTemplate.from_template(template)

@extract.get("/ask")
async def ask_question(
    question: str,
    object_name: str,
    pg_db: AsyncSession = Depends(get_postgres_db),
    neo_session: AsyncSession = Depends(get_neo4j_session)
):
    student_behavior_query = """
    MATCH (n:Student)-[:APPEARS_IN]->(bb:BoundingBox)
    MATCH (b:Behavior)<-[:REPRESENTS]-(bb)
    MATCH (i:Image {object_name: $object_name})-[:HAS_BOUNDING_BOX]->(bb)
    MATCH (c:Classroom)<-[:BELONGS_TO]-(n:Student)
    RETURN n.student_code as student_code, b.name AS behavior_type, bb.x1 as x1, bb.x2 as x2, bb.y1 as y1, bb.y2 as y2, c.name as classroom
    """
    result = await neo_session.run(student_behavior_query, object_name=object_name,)
    student_behavior_records = await result.data()
    
    if not student_behavior_records:
        return {"answer": "Image not found"}
    
    student_codes = list({int(r['student_code']) for r in student_behavior_records})
    
    list_student_query = select(Student).where(Student.id.in_(student_codes))
    student_results = await pg_db.execute(list_student_query)
    students = student_results.scalars().all()
    student_map = {s.id: s for s in students}
    
    final_result = []
    for student_behavior in student_behavior_records:
        if int(student_behavior['student_code']) in student_map:
            student_detail = student_map[int(student_behavior['student_code'])]
            final_result.append({
                'x1': student_behavior['x1'],
                'x2': student_behavior['x2'],
                'y1': student_behavior['y1'],
                'y2': student_behavior['y2'],
                'student_code': student_behavior['student_code'],
                'behavior': student_behavior['behavior_type'],
                'full_name': student_detail.full_name,
                # 'date_of_birth': student_detail.date_of_birth,
                'gender': student_detail.gender,
                'address': student_detail.address
            })
    
    # return {"data": final_result}
    
    
    try:
        formatted_json = json.dumps(final_result, indent=2)
    
        chain = prompt_template | llm
    
        response = chain.invoke({
            "json_data": formatted_json,
            "user_question": question
        })
    
        return {
            "question": question,
            "answer": response["result"]
        }
    except Exception as e:
        return {"error": f"I couldn't translate that to a query: {str(e)}"}


@extract.post("/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    neo_session: AsyncSession = Depends(get_neo4j_session)
):
    
    # 1. Validation
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # 2. Upload minio
    file_bytes = await file.read()
    
    extension = file.filename.split(".")[-1]
    object_name = f"{hashlib.sha256(file_bytes).hexdigest()}.{extension}"
    upload_task = asyncio.to_thread(
        sync_minio_upload, file_bytes, object_name, file.content_type
    )
    
    # 3. Check image exist before upload to minio and run YOLO
    check_image_exist_query = """
    OPTIONAL MATCH (img:Image {object_name: $object_name})
    RETURN img IS NOT NULL AS exists
    """
    result = await neo_session.run(check_image_exist_query, object_name=object_name,)
    record = await result.single()
    
    if record["exists"]:
        return {"object_name": object_name}
        
    
    # 4. Run YOLO and merge results
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    behavior_detection_task = asyncio.to_thread(detect_behaviour, img)
    face_detection_task = asyncio.to_thread(detect_face, img)
    
    behaviour_detection_yolo_result, face_detection_yolo_result = await asyncio.gather(behavior_detection_task, face_detection_task)
    
    behavior_detection_results = convert_yolo_result(behaviour_detection_yolo_result)
    face_detection_results = convert_yolo_result(face_detection_yolo_result)
    face_behavior_results = match_behaviour_with_face(face_detection_results, behavior_detection_results)
    
    await upload_task
    
    # 5. Store Neo4j
    cypher = """
    // 1. Create/Match the Image node
    MERGE (img:Image {object_name: $object_name})
    
    // 2. Process each detection in the list
    WITH img
    UNWIND $detections AS det
    
    // 3. Create a unique BoundingBox node for this specific detection
    // We use a random UUID or combine properties to ensure uniqueness
    CREATE (box:BoundingBox {
        x1: det.x1, y1: det.y1, x2: det.x2, y2: det.y2
    })
    
    // 4. Link Image to BoundingBox
    MERGE (img)-[:HAS_BOUNDING_BOX]->(box)
    
    // 5. Link Student to BoundingBox
    WITH box, det
    MATCH (s:Student {student_code: det.student_code})
    MERGE (s)-[:APPEARS_IN]->(box)
    
    // 6. Link Behavior to BoundingBox
    WITH box, det
    MATCH (b:Behavior {name: det.behavior})
    MERGE (box)-[:REPRESENTS]->(b)
    """
    
    await neo_session.run(
        cypher, 
        object_name=object_name, 
        detections=face_behavior_results
    )
    
    return {"object_name": object_name}
        
    











#Trích xuất học sinh từ frame
@extract.get("/students/frame/{image_id}")
def extract_student_frame(image_id: str):
    extract_student_frame_response = {
        'image_id': 'STA001',
        'total_students': 100,
        'students': [
            {
                'student_code': '48001',
                'bbox': {
                    'x1': 1,
                    'y1': 1,
                    'x2': 1,
                    'y2': 1
                },
                'confidence': 7.1,
                'crop_image_id': '001'
            }
        ]
    }
    return extract_student_frame_response


@extract.get("/students/features/{image_id}", response_model= ExtractStudentActivitiesResponse)
def extract_student_activities(image_id: str):
    extract_student_activities_response = {
        
    }
    return extract_student_activities_response

@extract.get("/students/description?student-code=&begin-time&end-time=", response_model= ExtractStudentDescriptionResponse)
def extract_student_description(student_code: str, begin_time: str, end_time: str):
    extract_student_description_response={
        
    }
    return extract_student_description_response
    