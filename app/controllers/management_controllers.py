
from fastapi import APIRouter
from app.schemas.management_schemas import CreateStudentFromMetadataRequest, CreateStudentFromMetadataResponse, CreateStudentRequest, CreateStudentResponse, CreateUserRequest, CreateUserResponse, DeleteStudentFromMetadataResponse, DeleteStudentResponse, DeleteUserResponse, DetailStudentResponse, FindActivitiesStudentResponse, FindUserResponse, UpdateStudentFromMetadataRequest, UpdateStudentFromMetadataRespoonse, UpdateStudentRequest, UpdateStudentResponse, UpdateUserRequest, UpdateUserResponse, UserResponse

metadata= APIRouter(prefix="/metadata", tags=["Metadata"])


#5 Thêm 1 học sinh vào danh sách  
@metadata.post("/students/{student_code}", response_model = CreateStudentFromMetadataResponse)
def create_metadata_students(create_metadata_students_request: CreateStudentFromMetadataRequest, student_code: str):
    create_metadata_students_response = {
        'student_code': '01',
        'class_of_student': '6a1',
        'activities' : [
            {
                'type': 'eating',
                'img': ['anh1','anh2'],
                'des': 'abcs',
                'begin_time': '6:23',
                'end_time': '5:23'
            },
            {
                'type': 'stading',
                'img': ['anh1','anh2'],
                'des': 'qưe',
                'begin_time': '4:23',
                'end_time': '9:23'
            }
        ]
    }
    return create_metadata_students_response

#6 Sửa thông tin học sinh 
@metadata.put("/students/{student_code}", response_model = UpdateStudentFromMetadataRespoonse)
def update_metadata_students(update_metadata_students_request: UpdateStudentFromMetadataRequest, student_code: str):
    update_metadata_students_response = {
        'student_code': '48001',
        'class_of_student': '1a1'
    }
    return update_metadata_students_response

#7 Xóa học sinh 
@metadata.delete("/students/{student_code}", response_model= DeleteStudentFromMetadataResponse)
def delete_metadata_students(student_code: str):    
    return {"message":  f"Student {student_code} has been deleted."}



#18 19 20 21 Neo4j