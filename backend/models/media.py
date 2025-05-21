from pydantic import BaseModel
from typing import List, Optional

class MediaItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    keywords: List[str]
    db: str
    thumbnail_url: str
class SearchResponse(BaseModel):
    results: List[dict]
    total: int
    took: int