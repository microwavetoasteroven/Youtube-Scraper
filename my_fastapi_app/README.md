# my_fastapi_app
This is a minimal FastAPI project setup.

## Setting up venv
To create your python virtual environment and install dependencies, use:

./create_venv.sh

## Activate venv
To activate your venv, from root directory my_fastapi_app, use:
source ./venv/bin/activate

## Running the Application
To run the application, from root directoy my_fastapi_app, use:

uvicorn app.main:app --reload

## Run neo4j and login
docker-compose up -d
docker-compose down
http://localhost:7474
username: neo4j
password: password

## Testing
Run tests with pytest:

pytest
