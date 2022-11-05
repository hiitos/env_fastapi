from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user as user_model
import api.schemas.user as user_schema

from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.engine import Result
import datetime

# ============================= DBに対するCRUD操作を行う処理 ============================= 

# --------------------Create--------------------
async def create_user(
    # 引数としてスキーマ user_create: user_schema.userCreate を受け取り、DBモデルであるuser_model.userに変換する
    # db: AsyncSessionは、非同期処理を行う際に指定しなければいけない
    db: AsyncSession, user_create: user_schema.UserCreate
) -> user_model.User:

    user = user_model.User(**user_create.dict())
    db.add(user)
    # DBにコミットする
    await db.commit()
    # DB上のデータを元にuserインスタンス user を更新する（この場合、作成したレコードの id を取得する）
    # データベースからオブジェクトの最新データを取得する
    await db.refresh(user)
    # 作成したDBモデルを返却する
    return user

# --------------------Read--------------------
# User一覧の関数
async def get_users_all(db: AsyncSession) -> List[Tuple[int, str,str,str,str,str, datetime.datetime,datetime.datetime]]:
    result: Result = await (
        db.execute(
            select(
                user_model.User.user_id,
                user_model.User.name,
                user_model.User.nickname,
                user_model.User.email,
                user_model.User.adress,
                user_model.User.phonenumber,
                user_model.User.created_at,
                user_model.User.updated_at,
            )
        )
    )
    return result.all()

# 特定Userの関数
async def get_users_one(db: AsyncSession, user_id: int) -> Optional[user_model.User]:
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.user_id == user_id)
    )
    user: Optional[Tuple[user_model.User]] = result.first()
    return user[0] if user is not None else None  # 要素が一つであってもtupleで返却されるので１つ目の要素を取り出す

# --------------------Update--------------------
async def update_user(
    db: AsyncSession, user_create: user_schema.UserCreate, original: user_model.User
) -> user_model.User:
    original.adress = user_create.adress
    original.updated_at = datetime.datetime.now()
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

# # --------------------Delete--------------------
async def delete_user(db: AsyncSession, original: user_model.User) -> None:
    await db.delete(original)
    await db.commit()
