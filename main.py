import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Film, Submission, Event, NewsItem, Sponsor, Update, NewsletterSubscription

app = FastAPI(title="St. Martin International Film Festival API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "St. Martin IFF API is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or "Unknown"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Utilities
class IdModel(BaseModel):
    id: str


def _to_str_id(doc):
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


# Films
@app.post("/api/films", response_model=dict)
def create_film(payload: Film):
    film_id = create_document("film", payload)
    return {"id": film_id}


@app.get("/api/films", response_model=List[dict])
def list_films(genre: Optional[str] = None, country: Optional[str] = None, category: Optional[str] = None):
    q = {}
    if genre:
        q["genre"] = genre
    if country:
        q["country"] = country
    if category:
        q["category"] = category
    docs = get_documents("film", q)
    return [_to_str_id(d) for d in docs]


# Submissions
@app.post("/api/submissions", response_model=dict)
def submit_film(payload: Submission):
    sub_id = create_document("submission", payload)
    return {"id": sub_id, "status": payload.status}


@app.get("/api/submissions", response_model=List[dict])
def list_submissions(status: Optional[str] = None):
    q = {"status": status} if status else {}
    docs = get_documents("submission", q)
    return [_to_str_id(d) for d in docs]


# Events / Program
@app.post("/api/events", response_model=dict)
def create_event(payload: Event):
    event_id = create_document("event", payload)
    return {"id": event_id}


@app.get("/api/events", response_model=List[dict])
def list_events(event_type: Optional[str] = None):
    q = {"type": event_type} if event_type else {}
    docs = get_documents("event", q)
    return [_to_str_id(d) for d in docs]


# News
@app.post("/api/news", response_model=dict)
def create_news(payload: NewsItem):
    nid = create_document("newsitem", payload)
    return {"id": nid}


@app.get("/api/news", response_model=List[dict])
def list_news():
    docs = get_documents("newsitem", {})
    return [_to_str_id(d) for d in docs]


# Sponsors
@app.post("/api/sponsors", response_model=dict)
def create_sponsor(payload: Sponsor):
    sid = create_document("sponsor", payload)
    return {"id": sid}


@app.get("/api/sponsors", response_model=List[dict])
def list_sponsors(tier: Optional[str] = None):
    q = {"tier": tier} if tier else {}
    docs = get_documents("sponsor", q)
    return [_to_str_id(d) for d in docs]


# Filmmaker Hub Updates
@app.post("/api/updates", response_model=dict)
def create_update(payload: Update):
    uid = create_document("update", payload)
    return {"id": uid}


@app.get("/api/updates", response_model=List[dict])
def list_updates(category: Optional[str] = None):
    q = {"category": category} if category else {}
    docs = get_documents("update", q)
    return [_to_str_id(d) for d in docs]


# Newsletter
@app.post("/api/newsletter", response_model=dict)
def subscribe_newsletter(payload: NewsletterSubscription):
    nid = create_document("newslettersubscription", payload)
    return {"id": nid}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
