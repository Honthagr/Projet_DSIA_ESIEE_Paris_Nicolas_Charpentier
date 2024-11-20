from pydantic import BaseModel

class User(BaseModel):
    name: str
    family_name: str
    email: str
    password: str
