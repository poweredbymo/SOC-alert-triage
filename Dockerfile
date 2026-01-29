# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Install system-level dependencies for XGBoost/OpenMP
RUN apt-get update && apt-get install -y \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code (app.py) and models folder into the container
COPY . .

# Expose the port FastAPI uses
EXPOSE 8000

# Start the uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]