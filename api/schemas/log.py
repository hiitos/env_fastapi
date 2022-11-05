import datetime
from typing import Optional
from pydantic import BaseModel, Field

# ============================= リクエスト・レスポンスの型を定義する ============================= 

class LogBase(BaseModel):
    content: Optional[str] = Field(None, example="ログのコンテンツ")
    content_int: Optional[int] = Field(None, example=100)

# Createのリクエストの型
class LogCreate(LogBase):
    pass

# Createのレスポンスの型
class LogCreateResponse(LogCreate):
    log_id: int
    user_id: int
    created_at: datetime.datetime = datetime.datetime.now()
    # DBと接続する際に使用
    class Config:
        orm_mode = True

# Updateの関数
# いらないと判断

# Readのレスポンスの型
class Log(LogBase):
    log_id: int
    user_id: int
    created_at: datetime.datetime 
    
    # DBと接続する際に使用
    class Config:
        orm_mode = True