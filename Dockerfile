# Dockerfile for Flask + SQL project
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables for Railway
ENV PORT=8080
ENV FLASK_ENV=production

# Expose port for Railway
EXPOSE 8080

# Run the Flask app
CMD ["python", "run.py"]
