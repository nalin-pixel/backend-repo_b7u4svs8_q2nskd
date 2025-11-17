import os
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Helpers ----------
class BookOut(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    description: str
    cover_url: Optional[str] = None
    buy_link: Optional[str] = None
    tags: List[str] = []
    featured: bool = False

class LoreOut(BaseModel):
    id: str
    title: str
    region: Optional[str] = None
    excerpt: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    tags: List[str] = []

class PostOut(BaseModel):
    id: str
    title: str
    excerpt: Optional[str] = None
    content: str
    cover_url: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = []
    published: bool = True


def _doc_to_model(doc) -> dict:
    if not doc:
        return {}
    d = dict(doc)
    _id = d.pop("_id", None)
    if isinstance(_id, ObjectId):
        d["id"] = str(_id)
    else:
        d["id"] = str(_id) if _id is not None else ""
    # Remove internal timestamps from response if present
    d.pop("created_at", None)
    d.pop("updated_at", None)
    return d


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/api/books", response_model=List[BookOut])
def list_books(featured: Optional[bool] = Query(None), limit: int = Query(12, ge=1, le=50)):
    try:
        from database import db
        if db is None:
            return []
        query = {}
        if featured is not None:
            query["featured"] = featured
        cursor = db["book"].find(query).sort("created_at", -1).limit(limit)
        return [_doc_to_model(doc) for doc in cursor]
    except Exception:
        return []

@app.get("/api/lore", response_model=List[LoreOut])
def list_lore(limit: int = Query(6, ge=1, le=50)):
    try:
        from database import db
        if db is None:
            return []
        cursor = db["lore"].find({}).sort("created_at", -1).limit(limit)
        return [_doc_to_model(doc) for doc in cursor]
    except Exception:
        return []

@app.get("/api/posts", response_model=List[PostOut])
def list_posts(published: bool = Query(True), limit: int = Query(3, ge=1, le=50)):
    try:
        from database import db
        if db is None:
            return []
        query = {"published": published}
        cursor = db["post"].find(query).sort("created_at", -1).limit(limit)
        return [_doc_to_model(doc) for doc in cursor]
    except Exception:
        return []


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
