from app.core.security import create_access_token, decode_access_token

# 1. Tạo Token cho user có id = 1
data_to_encode = {"sub": "1", "role": "admin"}
token = create_access_token(data=data_to_encode)
print(f"Token tạo ra: {token}\n")

# 2. Giải mã Token
decoded = decode_access_token(token)
print(f"Dữ liệu giải mã được: {decoded}")