
from pydantic import BaseModel
from typing import List, Optional

## Input and Output
class VideoCreate(BaseModel):
    content_id: str
    actual_label: str
    predicted_label: str
    feature_vector: List[float]
    tvshow: str

class VideoResponse(BaseModel):
    content_id: str
    actual_label: str
    predicted_label: str
    tvshow: str
    feature_vector: List[float]

    class Config:
        orm_mode = True