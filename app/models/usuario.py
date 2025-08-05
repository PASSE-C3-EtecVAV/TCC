from app import mysql
from werkzeug.security import check_password_hash

class Usuario:
    def __init__(self, id, nome, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

    @staticmethod
    def buscar_por_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nome, email, senha, tipo FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            return Usuario(*resultado)
        return None

    def verificar_senha(self, senha_digitada):
        return check_password_hash(self.senha, senha_digitada)