import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def abrir_conexao():
    try:
        
        senha_banco = os.getenv("DB_PASSWORD","")

        conexao = psycopg2.connect(
            host="localhost",
            database="agenda",
            user="joney",
            password=senha_banco,
            port="5432"
        )
        return conexao
    
    except Exception as e:
        print(f"Conexão falhou devido ao erro crítico: {e}")
        return None