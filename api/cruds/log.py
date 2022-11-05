from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as log_model
import api.schemas.log as log_schema

from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.engine import Result
import datetime

# from logger import getLogger

# logger = getLogger(logger_name)

# ============================= DBに対するCRUD操作を行う処理 ============================= 

# --------------------Create--------------------
async def create_log(
    db: AsyncSession, user_id, log_create: log_schema.LogCreate
) -> log_model.Log:

    log = log_model.Log(user_id=user_id,**log_create.dict())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

# --------------------Read--------------------
# Log一覧の関数
async def get_logs_all(db: AsyncSession) -> List[Tuple[int, int,str,int, datetime.datetime]]:
    result: Result = await (
        db.execute(
            select(
                log_model.Log.log_id,
                log_model.Log.user_id,
                log_model.Log.content,
                log_model.Log.content_int,
                log_model.Log.created_at,
            )
        )
    )
    return result.all()

# 特定UserのLogの関数
async def get_logs_user(db: AsyncSession, user_id: int) -> List[Tuple[int, int,str,int, datetime.datetime]]:
    result: Result = await db.execute(
        select(
            log_model.Log.log_id,
            log_model.Log.user_id,
            log_model.Log.content,
            log_model.Log.content_int,
            log_model.Log.created_at,
        ).filter(log_model.Log.user_id == user_id)
    )
    return result.all()

# 特定Logの関数
async def get_log_one(db: AsyncSession, log_id: int) -> Optional[log_model.Log]:
    result: Result = await db.execute(
        select(log_model.Log).filter(log_model.Log.log_id == log_id)
    )
    log: Optional[Tuple[log_model.Log]] = result.first()
    return log[0] if log is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

# --------------------Update--------------------
# 特に必要なしと判断

# # --------------------Delete--------------------
async def delete_log(db: AsyncSession, original: log_model.Log) -> None:
    await db.delete(original)
    await db.commit()
