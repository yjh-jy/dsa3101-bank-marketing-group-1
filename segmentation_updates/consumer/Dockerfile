# Use an official lightweight Python image
FROM python:3.10.6

# Set working directory inside the container
WORKDIR /app

# Copy dependencies first (optimizing Docker layer caching)
COPY ../requirements.txt /app/requirements.txt

# Install required Python libraries
RUN pip install -r requirements.txt

# Copy the entire producer codebase
COPY . .

# Run the producer script on container start
CMD ["python", "consumer/consumer.py"]