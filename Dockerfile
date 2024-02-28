# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the startup script into the container
# COPY startup_script.py /app/startup_script.py

# Copy the Python script into the container
COPY *.py /app/

# Run the Python script when the container launches
CMD ["python", "startup_script.py"]
