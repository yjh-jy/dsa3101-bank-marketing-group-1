# Use official Python image
FROM python:3.10-slim

# Set container's working directory to project root (/app)
WORKDIR /app

# Copy requirements first for caching
COPY customer_segmentation/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project (including nested folders)
COPY . .

# Create necessary directories
RUN mkdir -p customer_segmentation/visuals
RUN mkdir -p data/processed

# Command to run (path relative to WORKDIR /app)
CMD ["python", "customer_segmentation/scripts/segmentation.py"]