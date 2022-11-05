from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.user as user_crud
from api.db import get_db
import api.schemas.user as user_schema

router = APIRouter()

# ============================= リクエストが来た時のrouteと処理を記述 ============================= 

# --------------------Create--------------------
@router.post("/users", response_model=user_schema.UserCreateResponse)
async def create_user(
    # Depends は引数に関数を取り、 DI（Dependency Injection、依存性注入） を行う機構
    user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await user_crud.create_user(db, user_body)

"""
Request
UserCreateモデル(createのリクエストの型モデルを定義している関数)

{
    name: 'はなこ'
    nickname: 'はな'
    email: 'hanahana@gmail.com'
    adress: '東京都福生市'
    phonenumber: '07011503150'
}
"""

"""
Response
UserCreateResponseモデル(createのレスポンスの型モデルを定義している関数)

{
    name: 'はなこ'
    nickname: 'はな'
    email: 'hanahana@gmail.com'
    adress: '東京都福生市'
    phonenumber: '07011503150'
    user_id: '1'
    created_at: '2022-11-05'
    updated_at: '2022-11-05'
}
"""

# --------------------Read--------------------
# createされたUserの一覧を取得
@router.get("/users", response_model=List[user_schema.User])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_users_all(db)

"""
Request
全て取得なので、なし
"""

"""
Response
List[user_schema.User](Readのレスポンスの型モデルを定義している関数のリスト)

[
  {
    "name": "山田太郎01",
    "nickname": "やまちゃん01",
    "email": "sample01@gmail.com",
    "adress": "東京都福生市01",
    "phonenumber": "09012345678-01",
    "user_id": 1,
    "created_at": "2022-11-05T19:02:57",
    "updated_at": "2022-11-05T19:02:57"
  },
  {
    "name": "山田太郎02",
    "nickname": "やまちゃん02",
    "email": "sample02@gmail.com",
    "adress": "東京都福生市02",
    "phonenumber": "09012345678-02",
    "user_id": 2,
    "created_at": "2022-11-05T19:12:03",
    "updated_at": "2022-11-05T19:12:03"
  }
]
"""

# 特定のUserを取得
@router.get("/users/{user_id}", response_model=user_schema.User)
async def get_user_info(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_crud.get_users_one(db, user_id)

"""
Request
Userモデル(createのリクエストの型モデルを定義している関数)

{
    user_id: 2
}
"""

"""
Response
user_schema.User(Readのレスポンスの型モデルを定義している関数)

{
  "name": "山田太郎02",
  "nickname": "やまちゃん02",
  "email": "sample02@gmail.com",
  "adress": "東京都福生市02",
  "phonenumber": "09012345678-02",
  "user_id": 2,
  "created_at": "2022-11-05T19:12:03",
  "updated_at": "2022-11-05T19:12:03"
}
"""
# --------------------Update--------------------
@router.put("/users/{user_id}", response_model=user_schema.UserUpdateResponse)
async def update_user(
    user_id: int, user_body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_users_one(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.update_user(db, user_body, original=user)

"""
Request


{
  "name": "山田太郎",
  "nickname": "やまちゃん",
  "email": "sample@gmail.com",
  "adress": "東京都福生市",
  "phonenumber": "09012345678"
}
"""

"""
Response


"""

# # --------------------Delete--------------------
@router.delete("/users/{user_id}", response_model=None)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_users_one(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete_user(db, original=user)

"""
Request

{
    user_id: 2
}
"""

"""
Response
null
"""