import datetime
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.services.peloton import PelotonAPI
import os

def get_llm():
    return AzureChatOpenAI(
        model="gpt-4o",
        azure_deployment="gpt-4o",
        # openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        # azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_version="2024-08-01-preview",
    )

def get_workout_prompt():
    return PromptTemplate(
        input_variables=["user_goals", "workouts", "history", "profile","today_date"],
        template="""
        You are an experianced Peloton and fitness trainer task with creating a personalized weekly workout plan for users starting today {today_date}.
        Based on:
        - user's goals: {user_goals}, 
        - workouts that user can take: {workouts}, 
        - workout history: {history}, 
        - profile:  {profile}, 
        Create a personalized weekly workout plan for 4 weeks unless the user's goal specify otherwise. Include up to 5 activities in a day and make sure the workouts are aligned with the user's goals and offer good training value.
        Make sure to include a variety of classes to keep the user engaged and motivated and have rest day at least once a week. Rest day should have the title Rest Day. 
        Output is in json format ordered by days. The json output should have "week with a number" as the key and the value should be a list of week days with the following key:
        - "day" : the day of the week. use exact date.
        every day should have the following keys
        - "activities" : a list of dictionaries with the following keys
        - "title" : the title of the activity
        - "description" : the description of the activity
        - "category" : the category of the activity
        - "duration" : the duration of the activity in minutes
        - "instructor" : the name of the instructor
        - "intensity" : the intensity of the activity
        - "url" : the url of the activity
        - 'extra_info' : a detailed explanation on why this workout is beneficial for the user's goals.
        """
    )

def generate_workout_plan(client: PelotonAPI, user_goals: str):
    """
    Generate a workout plan using Peloton API and GPT-4.
    """
    # categories = client.get_workout_categories()
    
    cycling_workouts, cycling_instructors = client.get_last_rides("cycling", limit=200)
    strength_workouts, strength_instructors = client.get_last_rides("strength", limit=200)
    stretching_workouts, stretching_instructors = client.get_last_rides("stretching", limit=200)
    
    workouts = cycling_workouts + strength_workouts + stretching_workouts
    instructors = {instr["id"]: instr["name"] for instr in (cycling_instructors + strength_instructors + stretching_instructors)}
    new_workouts = []
    for workout in workouts:
        new_workout = {
            "url": "https://members.onepeloton.com/classes/all?modal=classDetailsModal&classId="+workout["id"],
            "title": workout["title"],
            "instructor": workout["instructor_id"],
            "description": workout["description"],
            "fitness_discipline": workout["fitness_discipline"],
            "duration_in_seconds": workout["duration"],
            "difficulty": workout["difficulty_estimate"],
        }
        new_workouts.append(new_workout)
    for workout in new_workouts:
        workout["instructor"] = instructors.get(workout["instructor"], "Unknown")
    history = client.get_workout_history()
    new_history = []
    for workout in history:
        new_workout = {
            "name": workout.get("name", "Unknown"),
            "taken_at": datetime.datetime.fromtimestamp(workout.get("start_time", 0)).strftime('%Y-%m-%d %H:%M:%S') if workout.get("start_time") else "Unknown",
            "fitness_discipline": workout.get("fitness_discipline", "Unknown"),
            "duration_in_seconds": workout.get("end_time", 0) - workout.get("start_time", 0) if workout.get("end_time") and workout.get("start_time") else 0,
            "difficulty": workout.get("effort_zones", {}).get("total_effort_points", "Unknown") if workout.get("effort_zones") else "Unknown",
            "heart_rate_zones": workout.get("effort_zones", {}).get("heart_rate_zone_durations", "Unknown") if workout.get("effort_zones") else "Unknown",
        }
        new_history.append(new_workout)
    profile = client.get_user_profile()

    # category_names = [cat["name"] for cat in categories]
    llm = get_llm().with_structured_output(method="json_mode")
    chain = get_workout_prompt() | llm
    
    input_data = {
    'user_goals':user_goals,
        'workouts':new_workouts,
        'history':new_history,
        'profile':profile,
        'today_date':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}

    content = chain.invoke(
        input=input_data,
    )
    return content
