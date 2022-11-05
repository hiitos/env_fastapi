import datetime
from typing import Optional
from pydantic import BaseModel, Field

# ============================= リクエスト・レスポンスの型を定義する ============================= 

class UserBase(BaseModel):
    name: Optional[str] = Field(None, example="山田太郎")
    nickname: Optional[str] = Field(None, example="やまちゃん")
    email: Optional[str] = Field(None, example="sample@gmail.com")
    adress: Optional[str] = Field(None, example="東京都福生市")
    phonenumber: Optional[str] = Field(None, example="09012345678")

# Createのリクエストの型
class UserCreate(UserBase):
    pass

# Createのレスポンスの型
class UserCreateResponse(UserCreate):
    user_id: int
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = Field(None)
    # DBと接続する際に使用
    class Config:
        orm_mode = True

# Updateの関数
class UserUpdateResponse(UserCreate):
    user_id: int
    updated_at: datetime.datetime = datetime.datetime.now()
    # DBと接続する際に使用
    class Config:
        orm_mode = True

# Readのレスポンスの型
class User(UserBase):
    user_id: int
    created_at: datetime.datetime 
    updated_at: datetime.datetime
    
    # DBと接続する際に使用
    class Config:
        orm_mode = True