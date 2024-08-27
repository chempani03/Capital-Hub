# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install necessary system packages
RUN apt-get update && apt-get install -y netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install dependencies from requirements.txt and additional packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
