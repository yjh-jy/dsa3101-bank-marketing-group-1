# Use an official Python image
FROM python:3.10.6

# Set working directory inside the container
WORKDIR /app

# Copy dependencies first (optimizing Docker layer caching)
COPY ../requirements.txt /app/requirements.txt

# Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire codebase
COPY . .