from pydantic import BaseModel
from typing import List

class WorkoutPlanRequest(BaseModel):
    user_goals: str

class WorkoutPlanResponse(BaseModel):
    weekly_plan: List[str]
