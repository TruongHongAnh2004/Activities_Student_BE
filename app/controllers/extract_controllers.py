import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.student import Student
from app.schemas.management_schemas import ExtractStudentActivitiesResponse, ExtractStudentDescriptionResponse, ExtractStudentFromFrameResponse
from app.yolo_behaviour_detection import detect_behaviour
from app.yolo_face_dectection import detect_face
from app.yolo_helper import match_behaviour_with_face

extract = APIRouter(prefix="/extract", tags= ["ExtractYolo"])
script_dir = os.path.dirname(os.path.abspath(__file__))

#Trích xuất học sinh từ frame
@extract.get("/students/frame/{image_id}")
def extract_student_frame(image_id: str, db: Session = Depends(get_db)):
    behaviour_detection_results = detect_behaviour(os.path.join(script_dir, '13.jpg'))
    face_detection_results = detect_face(os.path.join(script_dir, '13.jpg'))
    yolo_results = match_behaviour_with_face(face_detection_results, behaviour_detection_results)
    
    student_codes = map(lambda face: face['name'], face_detection_results)
    students = db.query(Student).filter(Student.id.in_(student_codes)).all()
    student_dict = {str(item.id): item for item in students}
    
    print(student_dict)
    
    results = []
    for result in yolo_results:
        if result['student_code'] not in student_dict:
            continue
        
        student = student_dict[result['student_code']]
        result['full_name'] = student.full_name
        result['gender'] = student.gender
        result['address'] = student.address
        result['date_of_birth'] = student.date_of_birth
        
        results.append(result)
        
        
    
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
            
        ],
        'results': results
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
    