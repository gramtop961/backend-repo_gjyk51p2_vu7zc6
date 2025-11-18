"""
Database Schemas for St. Martin International Film Festival

Each Pydantic model maps to a MongoDB collection using the lowercase
class name as the collection identifier.

Examples:
- Film -> "film"
- Submission -> "submission"
- Event -> "event"
"""
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime


class Film(BaseModel):
    title: str = Field(..., description="Film title")
    synopsis: Optional[str] = Field(None, description="Short synopsis")
    director: str = Field(..., description="Director name")
    country: Optional[str] = Field(None, description="Country of production")
    year: Optional[int] = Field(None, ge=1900, le=2100)
    genre: Optional[str] = None
    duration_min: Optional[int] = Field(None, ge=1)
    category: Optional[str] = Field(
        None,
        description="Programming category (Feature Films, Short Films, Docs, Student, Caribbean Spotlight)",
    )
    trailer_url: Optional[HttpUrl] = None
    stills: Optional[List[HttpUrl]] = Field(default=None, description="Image URLs")
    press_kit_url: Optional[HttpUrl] = None
    director_bio: Optional[str] = None
    director_contact: Optional[EmailStr] = None


class Submission(BaseModel):
    title: str
    director: str
    email: EmailStr
    country: Optional[str] = None
    category: str = Field(..., description="Submission category")
    duration_min: Optional[int] = Field(None, ge=1)
    synopsis: Optional[str] = None
    screener_link: Optional[str] = Field(None, description="Private link to the film screener")
    status: str = Field("received", description="received | in_review | selected | rejected")


class Venue(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=0)
    map_link: Optional[HttpUrl] = None


class Event(BaseModel):
    title: str
    film_id: Optional[str] = Field(None, description="Related film document id as string")
    type: str = Field(..., description="screening | gala | workshop | panel | market | networking")
    venue: Optional[str] = None
    starts_at: datetime
    ends_at: datetime
    description: Optional[str] = None


class NewsItem(BaseModel):
    title: str
    content: str
    cover_image: Optional[HttpUrl] = None
    published_at: datetime = Field(default_factory=datetime.utcnow)
    tags: Optional[List[str]] = None


class Sponsor(BaseModel):
    name: str
    tier: str = Field(..., description="title | presenting | gold | silver | partner | media")
    logo_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None


class Update(BaseModel):
    title: str
    message: str
    published_at: datetime = Field(default_factory=datetime.utcnow)
    category: Optional[str] = Field(None, description="workshop | panel | notice | market | accreditation")


class NewsletterSubscription(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    language: Optional[str] = Field("en", description="en | fr | es")
