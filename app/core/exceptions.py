import traceback
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# 1. Bắt lỗi HTTPException (400, 401, 403, 404...)
def custom_http_exception_handler(request: Request, ex: HTTPException):
    return JSONResponse(
        status_code=ex.status_code,
        content={
            "success": False,
            "status_code": ex.status_code,
            "detail": ex.detail
        }
    )

# 2. Bắt lỗi Validation dữ liệu (422)
def validation_exception_handler(request: Request, ex: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "status_code": 422,
            "detail": "Dữ liệu đầu vào không hợp lệ!",
            "errors": ex.errors()
        }
    )

# 3. Bắt lỗi Server nội bộ (500) - Đã thêm in Traceback ra Terminal
def global_exception_handler(request: Request, ex: Exception):
    print("\n" + "="*20 + " LỖI SERVER CHI TIẾT " + "="*20)
    traceback.print_exc()
    print("="*61 + "\n")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "status_code": 500,
            "detail": str(ex)  # Trả về nguyên nhân lỗi trực tiếp ra màn hình
        }
    )