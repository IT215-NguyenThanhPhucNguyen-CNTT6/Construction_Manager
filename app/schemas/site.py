from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

# Base Schema cho Công trình
class SiteBase(BaseModel):
    name: str
    code: str
    address: str | None = None
    description: str | None = None

# Input khi tạo mới công trình
class SiteCreate(SiteBase):
    pass

# Input khi cập nhật thông tin công trình
class SiteUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    description: str | None = None

# Output thông tin công trình
class SiteResponse(SiteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Input khi thêm thành viên vào công trình
class SiteMemberAdd(BaseModel):
    user_id: int
    role: str = "member"  # manager, supervisor, member

# Output thông tin thành viên công trình
class SiteMemberResponse(BaseModel):
    id: int
    site_id: int
    role: str
    joined_at: datetime
    user: UserResponse | None = None

    class Config:
        from_attributes = True