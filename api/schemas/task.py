from typing import Optional
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="クリーニングを取りに行く")

class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int
    # DBと接続する際に使用
    class Config:
        orm_mode = True

class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")
    # DBと接続する際に使用
    class Config:
        orm_mode = True