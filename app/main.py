import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.dependencies import get_peloton_client
from app.api.routes import router
from app.services.planner import generate_workout_plan
from app.services.peloton import PelotonAPI

app = FastAPI(
    title="Peloton Workout Planner",
    description="Generate a personalized weekly workout plan using Peloton and GPT-4.",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add API routes
app.include_router(router)

# Template renderer
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def render_form(request: Request):
    """
    Render the user input form.
    """
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/calendar", response_class=HTMLResponse)
async def render_calendar(
    request: Request,
    user_goals: str = Form(...)
):
    """
    Generate the workout plan and render it on the calendar page.
    """
    try:
        # Authenticate and generate the plan
        username = os.getenv("PELOTON_USERNAME")
        password = os.getenv("PELOTON_PASSWORD")
        client = get_peloton_client(username=username, password=password)
        plan = generate_workout_plan(client, user_goals)

        # Pass the plan to the calendar template
        return templates.TemplateResponse(
            "calendar.html", {"request": request, "weekly_plan": plan}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "form.html", {"request": request, "error": str(e)}
        )
