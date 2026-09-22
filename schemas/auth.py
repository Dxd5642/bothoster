from pydantic import BaseModel, EmailStr, Field

class RegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)

class LoginRequest(BaseModel):
    login: str
    password: str = Field(min_length=8, max_length=255)

class VeriryEmailRequest(BaseModel):
    email: EmailStr



# ==================================


class LoginResponse(BaseModel):
    username: str
    email: str

class MeResponse(BaseModel):
    username: str
    email: str

