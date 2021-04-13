from typing import Optional
from pydantic import BaseModel


class SearchFilter(BaseModel):
    query: Optional[str] = None
    data_type: Optional[str] = None


class CheckFilter(BaseModel):
    query: Optional[str] = None
    result: Optional[str] = None


class SuggestionFilter(BaseModel):
    query: Optional[str] = None
