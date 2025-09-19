FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && apt-get clean

WORKDIR /app

# Definir variáveis de ambiente para o mysqlclient
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mariadb"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmariadb"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PORT 5000
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "app:create_app()"]