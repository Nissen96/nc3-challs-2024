# Use Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app /app

# Install dependencies
RUN pip install flask pillow gunicorn

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0", "app:app"]
