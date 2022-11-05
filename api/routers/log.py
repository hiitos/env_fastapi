from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.log as log_crud
import api.cruds.user as user_crud
from api.db import get_db
import api.schemas.log as log_schema

router = APIRouter()

# ============================= リクエストが来た時のrouteと処理を記述 ============================= 

# --------------------Create--------------------
@router.post("/logs/{user_id}", response_model=log_schema.LogCreateResponse)
async def create_log(
    # Depends は引数に関数を取り、 DI（Dependency Injection、依存性注入） を行う機構
    user_id:int , log_body: log_schema.LogCreate, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_users_one(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await log_crud.create_log(db, user_id, log_body)

"""
Request
LogCreateモデル(createのリクエストの型モデルを定義している関数)

{
    user_id: 1
    content: 'ログのコンテンツ'
    content_int: 100
}
"""

"""
Response
LogCreateResponseモデル(createのレスポンスの型モデルを定義している関数)

{
    log_id: 1
    user_id: 1
    content: 'ログのコンテンツ'
    content_int: 100
    created_at: ""
}
"""

# --------------------Read--------------------
# createされたLogの一覧を取得
@router.get("/logs", response_model=List[log_schema.Log])
async def list_logs(db: AsyncSession = Depends(get_db)):
    return await log_crud.get_logs_all(db)

"""
Request
全て取得なので、なし
"""

"""
Response
List[log_schema.Log](Readのレスポンスの型モデルを定義している関数のリスト)

[
  {
    log_id: 1
    user_id: 1
    content: 'ログのコンテンツ'
    content_int: 100
    created_at: ""
  },
  {
    log_id: 2
    user_id: 2
    content: 'ログのコンテンツ'
    content_int: 100
    created_at: ""
  }
]
"""

# 特定のuserのLogを取得
@router.get("/logs/{user_id}", response_model=List[log_schema.Log])
async def get_log_info(user_id: int, db: AsyncSession = Depends(get_db)):
    
    user = await user_crud.get_users_one(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await log_crud.get_logs_user(db, user_id)

"""
Request
Logモデル(createのリクエストの型モデルを定義している関数)

{
    log_id: 2
}
"""

"""
Response

[
  {
    content: "ログのコンテンツ02",
    content_int: 100,
    log_id: 2,
    user_id: 1,
    created_at: "2022-11-05T22:30:18"
  },
  {
    content: "ログのコンテンツ03",
    content_int: 100,
    log_id: 3,
    user_id: 1,
    created_at: "2022-11-05T22:30:21"
  }
]
"""
# --------------------Update--------------------
# 特に必要なしと判断

# # --------------------Delete--------------------
@router.delete("/logs/{log_id}", response_model=None)
async def delete_log(log_id: int, db: AsyncSession = Depends(get_db)):
    log = await log_crud.get_log_one(db, log_id=log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")

    return await log_crud.delete_log(db, original=log)

"""
Request

{
    log_id: 2
}
"""

"""
Response
null
"""