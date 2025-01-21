from fastapi import APIRouter, Depends, HTTPException, Request
from app.api.dependencies import get_peloton_client
from app.services.planner import generate_workout_plan
from app.schemas.workout import WorkoutPlanRequest, WorkoutPlanResponse
import os
import logging

router = APIRouter()

@router.post("/generate-plan")
async def generate_plan(
    request: WorkoutPlanRequest,
):
    """
    Generate a weekly workout plan using the Peloton API and GPT-4.
    """
    logging.debug(f"Received request: {request}")
    try:
        username = os.getenv("PELOTON_USERNAME")
        password = os.getenv("PELOTON_PASSWORD")
        client = get_peloton_client(username=username, password=password)
        plan = generate_workout_plan(
            client=client,
            user_goals=request.user_goals
        )
        return plan
    except Exception as e:
        logging.error(f"Error generating plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))