from fastapi import APIRouter
from app.schemas.management_schemas import FindActivitiesStudentResponse, UserResponse


users= APIRouter(prefix="/users", tags=["Users"])

#17 Tìm kiếm hoạt động 
@users.get("/activies", response_model= FindActivitiesStudentResponse)
def find_activities_student(type: str, begin_time: str, end_time: str):
    find_activities_student_response = {
    'student_code': '48001',
    'class_of_student': '2a1',
    'type_activity': ['đứng', 'ăn']
    }
    return find_activities_student_response

# Thông tin người dùng 
@users.get("/information", response_model= UserResponse)
def user_information(email: str):
    user_information_response = {
        'name': 'My My', 
        'email': 'anguyenvan@gmail.com',
        'role': 'Giao Vien'
    }
    return user_information_response