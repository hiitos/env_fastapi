from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import api.cruds.task as task_crud
from api.db import get_db
import api.schemas.task as task_schema

router = APIRouter()

# --------------------Read--------------------
# リクエストパラメータやリクエストボディは取らないので、レスポンスだけを定義
# @router.get("/tasks", response_model=List[task_schema.Task])
# async def list_tasks():
#     return [task_schema.Task(id=1, title="1つ目のTODOタスク")]
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)


# --------------------Create--------------------
# ** をつけることで、 dict をキーワード引数として展開し、 task_schema.TaskCreateResponse クラスのコンストラクタに対して dict のkey/valueを渡します。
# = task_schema.TaskCreateResponse(id=1, title=task_body.title, done=task_body.done) と等価
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(
    # Depends は引数に関数を取り、 DI（Dependency Injection、依存性注入） を行う機構
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    return await task_crud.create_task(db, task_body)


# --------------------Update--------------------
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)

# --------------------Delete--------------------
@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)