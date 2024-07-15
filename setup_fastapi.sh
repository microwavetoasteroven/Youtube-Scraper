#!/bin/bash

# Define project name
PROJECT_NAME="my_fastapi_app"

# Create project directory
mkdir $PROJECT_NAME
cd $PROJECT_NAME

# Create app directory and initial files
mkdir -p tests/tests app/util
touch app/__init__.py tests/__init__.py

# Create main FastAPI application file
cat << EOF > app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
EOF

# Create dependencies file
touch app/dependencies.py

# Create a basic test file
cat << EOF > tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
EOF

# Create requirements.txt
cat << EOF > requirements.txt
fastapi
uvicorn[standard]
pytest
google-api-python-client
EOF

# Create a .gitignore file
cat << EOF > .gitignore
/venv
__pycache__/
*.pyc
.env
.DS_Store
EOF

# Create .env
cat << EOF > .env
# Environment variables
EOF

# Create config file
cat << EOF > app/config.py
# Configuration settings
EOF

# Create README.md
cat << EOF > README.md
# $PROJECT_NAME
This is a minimal FastAPI project setup.

## Running the Application
To run the application, use:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

## Testing
Run tests with pytest:
\`\`\`bash
pytest
\`\`\`
EOF

# Setup Python virtual environment
python3 -m venv venv

# Install Python packages
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

echo "Setup completed. Virtual environment created and dependencies installed."
echo "To activate the virtual environment, run:"
echo "source $PROJECT_NAME/venv/bin/activate"
