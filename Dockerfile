# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY healthcheck_script.py /app/healthcheck_script.py

# Run the Python script when the container launches
CMD ["python", "healthcheck_script.py"]