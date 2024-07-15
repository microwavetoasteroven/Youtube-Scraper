# Setup Python virtual environment
python3 -m venv venv

# Install Python packages
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

echo "Setup completed. Virtual environment created and dependencies installed."
echo "To activate the virtual environment, run:"
echo "source my_fastapi_app/venv/bin/activate"
