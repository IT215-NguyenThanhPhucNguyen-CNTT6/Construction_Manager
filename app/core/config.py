from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Cấu hình Database
    DATABASE_URL: str  # Đọc trong .env

    # Cấu hình JWT
    SECRET_KEY: str   # Đọc trong .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Cấu hình CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Khởi tạo Singleton instance
settings = Settings()