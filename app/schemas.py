# request-service/app/schemas.py
from pydantic import BaseModel

# リクエスト作成時の入力データ
class RequestCreate(BaseModel):
    title: str
    artist: str
    requester_name: str
    # is_played はDB側でデフォルト値Falseを持つため入力不要

# DBから取得したリクエストのデータ構造
class Request(RequestCreate):
    id: int
    is_played: bool
    
    class Config:
        # ORMモードを有効にすることで、SQLAlchemyモデルからPydanticモデルに変換可能にする
        from_attributes = True
