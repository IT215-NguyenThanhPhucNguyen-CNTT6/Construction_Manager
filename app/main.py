from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import Base, engine, get_db
from app.core.exceptions import (custom_http_exception_handler, validation_exception_handler, global_exception_handler)
from app.routers import auth, user

app = FastAPI(title="Quản lý công trình")

app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.include_router(auth.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

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