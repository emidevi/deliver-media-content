from fastapi import FastAPI, Query
from typing import List
from backend.models.media import MediaItem
from backend.utils.es import get_elastic

app = FastAPI()
es = get_elastic()

def normalize_hit(doc):
    media_id = str(doc.get("media_id", "")).zfill(10)
    db = doc.get("db", "st")
    base_url = "https://www.imago-images.de/bild"
    thumbnail_url = f"{base_url}/{db}/{media_id}/s.jpg"

    return {
        "id": media_id,
        "title": doc.get("title", "Untitled"),
        "description": doc.get("description", ""),
        "keywords": doc.get("keywords", []),
        "db": db,
        "thumbnail_url": thumbnail_url,
    }

@app.get("/search", response_model=List[MediaItem])
def search(q: str = Query("", description="Search keyword"), limit: int = 20):
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["title^2", "description", "keywords"]
            }
        },
        "size": limit
    }
    
    res = es.search(index="imago", body=query)
    return [normalize_hit(hit["_source"]) for hit in res["hits"]["hits"]]