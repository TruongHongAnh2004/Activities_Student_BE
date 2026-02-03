
from fastapi import APIRouter

from app.schemas.management_schemas import CreateUserRequest, CreateUserResponse, DeleteUserResponse, FindUserResponse, UpdateUserRequest, UpdateUserResponse, UserResponse


admin= APIRouter(prefix="/admin", tags=["Admin"])

#12 Xem toàn bộ người dùng 
@admin.get("/users",response_model= list[UserResponse])
def get_all_users():
    users = [
        {'name': 'nguyen an', 
        'email': 'annguyen@gmail.com',
        'role': 'teacher'},
        {'name': 'nguyen bi', 
        'email': 'binguyen@gmail.com',
        'role': 'teacher'}
    ]
    return users

    
#13 Tìm kiếm người dùng
@admin.get("/find-users", response_model= FindUserResponse)
def find_user(name: str, role: str):
    find_user_response = {
       'name': ['hong anh', 'my anh', 'phuong', 'thanh', 'thu'],
       'role':['admin','teacher','teacher','teacher','teacher']
    }
    return find_user_response

#14 Tạo người dùng 
@admin.post("/user", response_model =CreateUserResponse)
def create_user(create_user_request: CreateUserRequest):
    create_user_response = {
        'name': 'tranvangiau'
    }
    return create_user_response

#15 Xoá người dùng
@admin.delete("/users/{id}", response_model= DeleteUserResponse)
def delete_user(id: str):
    return {"message": f"User with id {id} has been deleted."}

#16 Sửa thông tin người dùng 
@admin.put("/users/{id}", response_model=UpdateUserResponse)
def update_user(update_user_request: UpdateUserRequest, id: str):
    update_user_response={
        'name': 'teddy'
    }
    return update_user_response