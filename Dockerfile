# Dockerfile for Flask + SQL project
FROM python:3.11-slim

# Set work directory
WORKDIR /app


# Instalar dependências do sistema para mysqlclient
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev build-essential

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
