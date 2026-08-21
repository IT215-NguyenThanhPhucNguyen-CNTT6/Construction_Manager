from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

# Base Schema cho Hạng mục công việc
class WorkItemBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "pending"  # pending, in_progress, completed

# Input khi tạo hạng mục mới
class WorkItemCreate(WorkItemBase):
    site_id: int

# Input khi cập nhật hạng mục / trạng thái
class WorkItemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

# Output thông tin hạng mục
class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    created_by: int
    created_at: datetime
    created_by_user: UserResponse | None = None

    class Config:
        from_attributes = True