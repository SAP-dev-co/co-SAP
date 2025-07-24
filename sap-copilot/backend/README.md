# Setting up the Backend

## Step 1: Make Sure you are the in the backend directory if not alrealy 
``` bash
cd backend
```

## Step 2: Create and Activate the Virtual Environment
``` bash
python -m venv venv
.\venv\Scripts\Activate
```

## Step 3: Install all necessary libraries  
``` bash
pip install fastapi uvicorn langchain google-generativeai pylint python-dotenv
```

## Step 4: Just in case install again
``` bash
pip install -r requirements.txt
```