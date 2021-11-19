# QuickEx

A simple content management system.

## Tech stack
- Flask
- PostgreSQL
- SQLite

## Getting started
It is recommended to use the virtual environment feature. Here are steps to create virtual environment and install the requirements.

#### Virtual environment
1. Create virtual environment: `python -m venv .venv`
2. Activate virtaul environment:
   1. Windows: `.venv/Scripts/activate.bat`
   2. Linux: `.venv/bin/activate`
3. Install requirments: `pip install -r requirements.txt`

### How to start app?
Below are steps to start the application:
#### On Linux
 `FLASK_APP=app.py FLASK_ENV=development flask run`

#### On windows
To run application on windows, you need to perform below steps.
1. Create environment variable to set application's start file: `set FLASK_APP=app.py`
2. Create environment variable to set application's environment: `set FLASK_ENV=development`
3. Start the application: `flask run`

#### App URL
http://localhost:5000/

#### API endpoint
http://localhost:5000/api/test
