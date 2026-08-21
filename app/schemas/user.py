from pydantic import BaseModel, EmailStr
from datetime import datetime

# Base schema chứa các trường chung
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None

# Input khi Đăng ký tài khoản
class UserCreate(UserBase):
    password: str

# Input khi Đăng nhập
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Output trả về thông tin User (ẩn password)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Cho phép đọc dữ liệu trực tiếp từ SQLAlchemy ORM Model