# Use Python image
FROM python:3.10.6

# Set working directory inside the container
WORKDIR /campaign_optimization

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (this runs the producer by default)
CMD ["python", "scripts/real_time_date.py"]