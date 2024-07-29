Project name : fastapi-app-jwt

Python Fastapi project based on registration user,login and Authentication and Authorization factors.

## DESCRIPTION
This is a simple example how to create a users and to login in a service with the Authentication and Authorization with JWT(Json Web Token) concept.

## INSTALLATION
Clone the repository with:
git clone https://github.com/Marco-Aurelio90/fastapi-app-jwt.git

## PROJECT DIRECTORY
cd (project name) 
example : cd fastapi-app-jwt

## CREATE ENVIROMENT VARIABLE 
python -m venv env

## ACTIVATE THE ENV VARIABLE 
On Windows
.\env\Scripts\activate

# On macOS/Linux
source env/bin/activate

## INSTALL DEPENDENCY
pip install -r requirements.txt

## EXECUTE THE APP
uvicorn main:app --reload

In this case you should write the name of the app as: 

uvicorn app:app --reload

You can now access the application by opening a browser and navigating to http://127.0.0.1:8000, after put a /docs as endpoint of the application

