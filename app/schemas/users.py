# app/schemas/users.py ichiga qo'shing:
class UserLogin(BaseModel):
    phone_number: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str