from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import Base, engine, get_db
from app.core.exceptions import custom_http_exception_handler

app = FastAPI(title="Quản lý công trình")

# Đăng ký custom exception handler
app.add_exception_handler(HTTPException, custom_http_exception_handler)

# Tạo bảng
Base.metadata.create_all(bind=engine)


# Health check endpoint kèm kiểm tra DB
@app.get("/health", tags=["Health Check"])
def check_health(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "ok",
        "database": db_status
    }