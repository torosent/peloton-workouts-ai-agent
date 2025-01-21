from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    weight: Optional[float]
    height: Optional[float]
    age: Optional[int]
    gender: Optional[str]
