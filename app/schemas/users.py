from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id:int
    email: EmailStr
    
    
    class Config:
        from_attributes = True