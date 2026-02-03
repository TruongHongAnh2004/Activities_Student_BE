from pydantic import BaseModel
from typing import Optional
from typing import List


 #1 Lấy ảnh 
class ImageResponse(BaseModel):
    image_id: str
    filename: str
    content_type: str
    size: int
    url: str

#2 Trích xuất học sinh từ frame

class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class StudentDetection(BaseModel):
    student_code: str
    bbox: BoundingBox
    confidence: float
    crop_image_id: str | None = None

class ExtractStudentFromFrameResponse(BaseModel):
    image_id: str
    total_students: int
    students: List[StudentDetection]
    
#3 Trích xuất & nhận diện hành vi
class ExtractStudentActivitiesResponse(BaseModel): 
    image_id: str
    total_students: int
    students: List[StudentDetection]

#4 Trích xuất & tạo mô tả học sinh  
class ExtractStudentDescriptionResponse(BaseModel):
    student_code: str
    begin_time: str
    end_time: str
    
    summary: ExtractStudentActivitiesResponse
    description_text: str
    
#5 Thêm 1 học sinh vào danh sách 
class CreateStudentFromMetadataRequest(BaseModel):
    class_of_student: str

#class act
class Activity(BaseModel):
    type: str
    img: list[str]
    des: str
    begin_time: str
    end_time: str
     
class CreateStudentFromMetadataResponse(BaseModel):
    student_code: str
    class_of_student: str
    activities: list[Activity]

#6 Sửa thông tin học sinh
class UpdateStudentFromMetadataRequest(BaseModel):
    class_of_student: str

class UpdateStudentFromMetadataRespoonse(BaseModel):
    student_code: str
    class_of_student: str
    
#7 Xóa học sinh     
class DeleteStudentFromMetadataResponse(BaseModel):
    message: str
    
#8 Xem chi tiết dữ liệu của hocj sinh
class DetailStudentResponse(BaseModel):
    student_code: str 
    full_name: str
    date_of_birth: str
    metadata: str
    gender: str
    address: str
    
#9 Sửa dữ liệu của hoc sinh
class UpdateStudentRequest(BaseModel): 
    full_name: str
    date_of_birth: str
    gender: str
    address: str

class UpdateStudentResponse(BaseModel):
    full_name: str
    date_of_birth: str
    metadata: str
    gender: str
    address: str

#10 Thêm dữ liệu vào hoc sinh
class CreateStudentRequest(BaseModel):
    student_code: str 
    full_name: str
    date_of_birth: str
    gender: str
    address: str
    
class CreateStudentResponse(BaseModel):
    student_code: str 
    full_name: str
    date_of_birth: str
    metadata: str
    gender: str
    address: str
    
#11 Xoá một dữ liệu trong hoc sinh
class DeleteStudentResponse(BaseModel):
    message: str

#12 Xem toàn bộ người dùng (dùng chung 18)
class UserResponse(BaseModel):
    name: str 
    email: str
    role: str
    
#13 Tìm kiếm người dùng 
class FindUserResponse(BaseModel):
    name: List[str] #PHAI TRA 1 LIST TEN 
    role: List[str]
#14 Tạo người dùng 
class CreateUserRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    role: str | None = None
    password: str | None = None

class CreateUserResponse(BaseModel):
    name: str | None = None
    
    
#15 Xoá người dùng
class DeleteUserResponse(BaseModel):
    message: str
    
#16 Sửa thông tin người dùng
class UpdateUserRequest(BaseModel):
    name: str
    email: str
    
class UpdateUserResponse(BaseModel):
    name: str
   

#17 Tìm kiếm hoạt động 
class FindActivitiesStudentResponse(BaseModel):
    student_code: str
    class_of_student: str
    type_activity: List[str]
    
# #18 Thông tin người dùng
# class UserInformationRequest(BaseModel):
#     email: str
    
