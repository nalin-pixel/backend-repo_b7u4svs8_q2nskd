"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# ---------- Site Schemas ----------
class Book(BaseModel):
    title: str = Field(..., description="Book title")
    subtitle: Optional[str] = Field(None, description="Optional subtitle")
    description: str = Field(..., description="Short blurb/description")
    cover_url: Optional[str] = Field(None, description="URL to cover image")
    buy_link: Optional[str] = Field(None, description="External link to purchase")
    tags: List[str] = Field(default_factory=list, description="Genres or tags")
    featured: bool = Field(False, description="Show as featured on homepage")

class Lore(BaseModel):
    title: str = Field(..., description="Lore entry title")
    region: Optional[str] = Field(None, description="Kingdom/region/faction")
    excerpt: Optional[str] = Field(None, description="Short overview")
    content: str = Field(..., description="Full lore content (markdown allowed)")
    image_url: Optional[str] = Field(None, description="Optional illustration URL")
    tags: List[str] = Field(default_factory=list, description="Categories/tags")

class Post(BaseModel):
    title: str = Field(..., description="Blog post title")
    excerpt: Optional[str] = Field(None, description="Short summary for listings")
    content: str = Field(..., description="Full post content (markdown allowed)")
    cover_url: Optional[str] = Field(None, description="Hero image for the post")
    author: Optional[str] = Field(None, description="Author display name")
    tags: List[str] = Field(default_factory=list, description="Tags for the blog post")
    published: bool = Field(True, description="Whether the post is published")

# ---------- Example Schemas (kept for reference) ----------
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
