# Peloton Workouts AI Agent

This AI agent generates a personalized weekly workout plan using Peloton’s API and GPT-4o. The agent will create a plan tailored to your workout history, physical attributes, and fitness goals. 

## TODO
- [ ] Add a durable framework to run at scale.
- [ ] Add prompt options with categories such as cycling, running, rowing, etc.
- [ ] Add persistent data store.
- [ ] Add cron jobs to analyze progress and adjust the plan.

> **Note:** This project is a proof of concept. A real AI agent would be able to schedule workouts, but the current APIs do not support this functionality.

## Project Structure

- **app/main.py**  
  Entry point for the FastAPI application.
- **app/api/routes.py**  
  Defines the `/generate-plan` endpoint for creating workout plans.
- **app/api/dependencies.py**  
  Sets up a `get_peloton_client` dependency.
- **app/services/peloton.py**  
  Interacts with the Peloton API.
- **app/services/planner.py**  
  Calls the Peloton API, processes user data, and invokes GPT-4 for plan creation.
- **app/templates**  
  HTML templates for rendering the form and calendar.
- **app/static**  
  Static assets (CSS, JS).
- **requirements.txt**  
  Python dependencies.
- **.env**  
  Specifies environment variables (see below).

## Setup

1. Clone or download the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file with the following variables:

| Variable                | Type   | Description                           |
|-------------------------|--------|---------------------------------------|
| AZURE_OPENAI_ENDPOINT   | string | The endpoint for Azure OpenAI (GPT-4o).|
| AZURE_OPENAI_API_KEY    | string | Azure OpenAI API key.                 |
| PELOTON_USERNAME        | string | Your Peloton account username.        |
| PELOTON_PASSWORD        | string | Your Peloton account password.        |

4. Run the server locally using Uvicorn:
```bash
uvicorn app.main:app --reload
```

## Usage
1.  Open http://127.0.0.1:8000/ in your browser.
2. Specify your fitness goals. 

### Example Prompts

Here are some example prompts you can use to specify your fitness goals:

- "I want to lose weight and tone my body."
- "I am training for a marathon and need a running plan."
- "I want to increase my flexibility and core strength."
- "I need a balanced workout plan that includes both cardio and strength training."
- "I want to improve my cycling performance."

3. Obtain your personalized workout plan in a calendar view.

## Legal Disclaimer

This project is not affiliated with, endorsed by, or in any way associated with Peloton Interactive, Inc. The use of Peloton’s API is for educational and proof-of-concept purposes only. All trademarks, service marks, and company names are the property of their respective owners. Use this project at your own risk. The authors are not responsible for any misuse or damage caused by this project.