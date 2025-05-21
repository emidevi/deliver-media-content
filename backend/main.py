from fastapi import FastAPI, Query, HTTPException
from typing import List
from backend.models.media import MediaItem, SearchResponse
from backend.utils.es import get_elastic
from elasticsearch.exceptions import ConnectionError
from elasticsearch import exceptions as es_exceptions
from backend.utils.logger import logging

app = FastAPI()
es = get_elastic()
logger = logging.getLogger(__name__)

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

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search", response_model=List[MediaItem])
def search(q: str = Query("", description="Search keyword"), 
           limit: int = Query(10, ge=1, le=100, description="Number of results"),
           offset: int = Query(0, ge=0, description="Result offset")):
    query = {
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["title^2", "description", "keywords"]
            }
        },
        "from": offset,
        "size": limit
    }

    try:
        res = es.search(index="imago", body=query)
        hits = res["hits"]["hits"]
        logger.info(f"Search successful: query='{q}', hits={len(hits)}")
        return [normalize_hit(hit["_source"]) for hit in res["hits"]["hits"]]
    
    except ConnectionError as e:
        logger.error(f"Elasticsearch connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
    
    except Exception as e:
        logger.exception("Unexpected error during search")
        raise HTTPException(status_code=500, detail="Internal server error.")
    
    except es_exceptions.ElasticsearchException as e:
        logger.error(f"Elasticsearch error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")