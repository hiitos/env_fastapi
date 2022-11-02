from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model
import api.schemas.task as task_schema

from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.engine import Result

# ============================= DBに対するCRUD操作を行う処理 ============================= 


# --------------------Create--------------------
async def create_task(
    # 引数としてスキーマ task_create: task_schema.TaskCreate を受け取り、DBモデルであるtask_model.Taskに変換する
    # db: AsyncSessionは、非同期処理を行う際に指定しなければいけない
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:

    task = task_model.Task(**task_create.dict())
    db.add(task)
    # DBにコミットする
    await db.commit()
    # DB上のデータを元にTaskインスタンス task を更新する（この場合、作成したレコードの id を取得する）
    # データベースからオブジェクトの最新データを取得する
    await db.refresh(task)
    # 作成したDBモデルを返却する
    return task

# --------------------Read--------------------
async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()

# --------------------Update--------------------
async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す


async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

# --------------------Delete--------------------
async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
