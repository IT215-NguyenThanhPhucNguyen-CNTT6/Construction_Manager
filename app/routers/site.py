from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.user import User
from app.models.site import ConstructionSite, SiteMember
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse, SiteMemberAdd, SiteMemberResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/construction-sites", tags=["Construction Sites"])

# Hàm phụ trợ: Kiểm tra thành viên & phân quyền
def check_site_access(site_id: int, user_id: int, db: Session, required_roles: Optional[List[str]] = None):
    site = db.query(ConstructionSite).filter(ConstructionSite.id == site_id).first()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Công trình không tồn tại!")
    
    member = db.query(SiteMember).filter(
        SiteMember.site_id == site_id, 
        SiteMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không phải thành viên công trình này!")
    
    if required_roles and member.role not in required_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền thực hiện thao tác này!")
    
    return site, member


# 1. Tạo công trình
@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
def create_site(site_in: SiteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(ConstructionSite).filter(ConstructionSite.code == site_in.code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã công trình đã tồn tại!")

    new_site = ConstructionSite(
        name=site_in.name,
        code=site_in.code,
        address=site_in.address,
        description=site_in.description,
        created_by=current_user.id
    )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    owner_member = SiteMember(site_id=new_site.id, user_id=current_user.id, role="OWNER")
    db.add(owner_member)
    db.commit()

    return new_site


# 2. Danh sách công trình
@router.get("", response_model=List[SiteResponse])
def get_sites(search: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(ConstructionSite).join(SiteMember).filter(SiteMember.user_id == current_user.id)
    
    if search:
        query = query.filter(ConstructionSite.name.ilike(f"%{search}%"))
        
    return query.all()


# 3. Chi tiết công trình
@router.get("/{site_id}", response_model=SiteResponse)
def get_site_detail(site_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    site, _ = check_site_access(site_id, current_user.id, db)
    return site


# 4. Cập nhật công trình
@router.put("/{site_id}", response_model=SiteResponse)
def update_site(site_id: int, site_in: SiteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    site, _ = check_site_access(site_id, current_user.id, db, required_roles=["OWNER", "MANAGER"])
    
    if site_in.name is not None: site.name = site_in.name
    if site_in.address is not None: site.address = site_in.address
    if site_in.description is not None: site.description = site_in.description
        
    db.commit()
    db.refresh(site)
    return site


# 5. Xóa công trình
@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    site, _ = check_site_access(site_id, current_user.id, db, required_roles=["OWNER"])
    db.delete(site)
    db.commit()
    return None


# 6. Thêm thành viên
@router.post("/{site_id}/members", status_code=status.HTTP_201_CREATED)
def add_member(site_id: int, member_in: SiteMemberAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_site_access(site_id, current_user.id, db, required_roles=["OWNER", "MANAGER"])

    if not db.query(User).filter(User.id == member_in.user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User không tồn tại!")

    if db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == member_in.user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Thành viên đã có trong công trình!")

    db.add(SiteMember(site_id=site_id, user_id=member_in.user_id, role=member_in.role))
    db.commit()
    return {"message": "Thêm thành viên thành công"}


# 7. Xóa thành viên
@router.delete("/{site_id}/members/{user_id}")
def remove_member(site_id: int, user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_site_access(site_id, current_user.id, db, required_roles=["OWNER"])

    target_member = db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.user_id == user_id).first()
    if not target_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thành viên không thuộc công trình này!")

    if target_member.role == "OWNER":
        if db.query(SiteMember).filter(SiteMember.site_id == site_id, SiteMember.role == "OWNER").count() <= 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa OWNER cuối cùng!")

    db.delete(target_member)
    db.commit()
    return {"message": "Xóa thành viên thành công"}


# 8. Danh sách thành viên
@router.get("/{site_id}/members", response_model=List[SiteMemberResponse])
def get_site_members(site_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    check_site_access(site_id, current_user.id, db)

    return db.query(
        User.id.label("user_id"),
        User.email,
        User.full_name,
        SiteMember.role,
        SiteMember.joined_at
    ).join(SiteMember, User.id == SiteMember.user_id).filter(SiteMember.site_id == site_id).all()