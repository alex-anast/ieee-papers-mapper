from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class Author(BaseModel):
    author_id: str
    full_name: str
    affiliation: str


class ProcessedPaper(BaseModel):
    is_number: str
    insert_date: str
    publication_year: str
    download_count: int = Field(ge=0)
    citing_patent_count: int = Field(ge=0)
    title: str = Field(min_length=1)
    abstract: str
    index_terms_ieee: list[str] = []
    index_terms_dynamic: list[str] = []
    authors: list[Author]
    prompt: str

    @field_validator("insert_date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        datetime.strptime(v, "%Y-%m-%d")
        return v


class ClassifiedPaper(BaseModel):
    paper_id: int
    category: str
    confidence: float = Field(ge=0.0, le=1.0)
