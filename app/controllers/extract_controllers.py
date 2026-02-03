from fastapi import APIRouter

from app.schemas.management_schemas import ExtractStudentActivitiesResponse, ExtractStudentDescriptionResponse, ExtractStudentFromFrameResponse
from app.yolo import detect_and_draw

extract = APIRouter(prefix="/extract", tags= ["ExtractYolo"])

@extract.get("/students/frame/{image_id}")
def extract_student_frame(image_id: str):
    detect_and_draw("./16_000489.jpg")
    extract_student_frame_response = {
        
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
    