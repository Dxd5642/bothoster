from pydantic import BaseModel, EmailStr, Field

class RegistrationRequest(BaseModel):
    username: str
    email: EmailStr | None 
    password: str = Field(min_length=8, max_length=255)

class LoginRequest(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=255)

class LoginResponse(BaseModel):
    username: str
    email: str

class MeResponse(BaseModel):
    username: str
    email: str