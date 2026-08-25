from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Schema Tạo công trình
class SiteCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    code: str = Field(..., min_length=1, max_length=50)
    address: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

# Schema Cập nhật công trình
class SiteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    address: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None

# Schema Thêm thành viên
class SiteMemberAdd(BaseModel):
    user_id: int
    role: str = Field("MEMBER", description="OWNER, MANAGER, SUPERVISOR, MEMBER")

# Schema Trả về thông tin Thành viên
class SiteMemberResponse(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str] = None
    role: str
    joined_at: datetime

    class Config:
        from_attributes = True

# Schema Trả về thông tin Công trình
class SiteResponse(BaseModel):
    id: int
    name: str
    code: str
    address: Optional[str]
    description: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True