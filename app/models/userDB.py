from sqlmodel import SQLModel, Field

#Struttura dati di User

class User(SQLModel, table=True):
    username : str = Field(primary_key=True)
    name : str
    email : str

class UserCreate(SQLModel):
    username: str
    name: str
    email:str




