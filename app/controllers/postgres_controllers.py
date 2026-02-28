from fastapi import APIRouter

from app.schemas.management_schemas import CreateStudentRequest, CreateStudentResponse, DeleteStudentResponse, DetailStudentResponse, FindStudentsResponse, UpdateStudentRequest, UpdateStudentResponse


postgres= APIRouter(prefix="/postgre", tags=["Postgre"])
#8**
@postgres.get("/find-students/data/", response_model= FindStudentsResponse)
def get_detail_student(student_code: str):
    find_students_reponse = {
        'student_code': ['48001', '48002','48003'],
        'class_of_student': "1a1"
    }
    return find_students_reponse
#8 Xem chi tiết dữ liệu của học sinh
@postgres.get("/students/data/{student_code}", response_model= DetailStudentResponse)
def get_detail_student(student_code: str):
    get_detail_student_reponse = {
        'student_code': 'abc1234',
        'full_name': 'abc',
        'date_of_birth': '14/4/2004',
        'metadata': 'abc',
        'gender': 'male',
        'address': 'abc'
    }
    return get_detail_student_reponse

#9 Sửa dữ liệu của học sinh
@postgres.put("/students/data/{student_code}", response_model= UpdateStudentResponse)
def update_data_students(update_data_students_resquest :UpdateStudentRequest, student_code: str):
    update_data_students_response = {
        'full_name': 'tony',
        'date_of_birth': '14/04/2004',
        'metadata': 'picpnj',
        'gender': 'male',
        'address': 'chanhhung'
    }
    return update_data_students_response

#10 Thêm dữ liệu vào học sinh 
@postgres.post("/students/data", response_model= CreateStudentResponse)
def create_data_students(create_data_students_request: CreateStudentRequest):
    create_data_students_response = {
        'student_code': '48001',
        'full_name': 'tony',
        'date_of_birth': '14/04/2004',
        'metadata': 'picpnj',
        'gender': 'male',
        'address': 'chanhhung'
    }
    return create_data_students_response

#11 Xoá một dữ liệu trong học sinh 
@postgres.delete("/students/data/{student_code}", response_model= DeleteStudentResponse)
def delete_data_students(student_code: str):    
    return {"message":  f"Student {student_code} has been deleted."}
