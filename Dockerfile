# Dockerfile for Flask + SQL project
FROM python:3.11-slim

# Set work directory
WORKDIR /app


# Instalar dependências do sistema para mysqlclient
RUN apt-get update && apt-get install -y gcc libmariadb-dev-compat libmariadb-dev build-essential python3-dev pkg-config

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
CMD ["python", "-m", "waitress", "--port=8080", "run:app"]
