from pydantic import BaseModel

# Output trả về Client khi đăng nhập thành công
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Dữ liệu giải mã từ JWT Token
class TokenData(BaseModel):
    email: str | None = None
    user_id: int | None = None