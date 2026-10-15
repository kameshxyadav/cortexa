# backend/app/models.py

from sqlmodel import SQLModel, Field
from typing import Optional

class Unit(SQLModel, table=True):
    """Content unit representing a chunk of source material.
    Locator fields vary by source kind (pdf, pptx, video, figure).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(index=True)
    source_id: int = Field(index=True)
    kind: str = Field(index=True)  # e.g., text, figure, table, transcript, slide, equation
    text: Optional[str] = None
    page: Optional[int] = None
    slide: Optional[int] = None
    t_start: Optional[int] = None  # start seconds for video
    t_end: Optional[int] = None
    bbox_json: Optional[str] = None
    image_path: Optional[str] = None
    caption: Optional[str] = None
    parent_heading: Optional[str] = None
    order_idx: Optional[int] = None
    token_count: Optional[int] = None
