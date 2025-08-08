import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações flask
    SECRET_KEY = os.getenv('SECRET_KEY')

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tcc'
    SECRET_KEY = 'senha_mucho_braba_123@$%&*'


    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')