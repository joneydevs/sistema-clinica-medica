from database import abrir_conexao
from queries import LISTAR_PACIENTES
import psycopg2

def lista_pacientes():
    conexao = abrir_conexao()
    if not conexao:
        return
   
    try:  

        cursor = conexao.cursor()  
        cursor.execute(LISTAR_PACIENTES)
        pacientes = cursor.fetchall()

        print("\n"+"="*100)
        print("                                     PACIENTES NO BANCO")
        print("="*100)

        for p in pacientes:
            print(f"esse é o ID: {p[0]:<4} | aqui é o NOME: {p[1]:<25} | {p[2]:<25} | {p[3]} ")

        
    except Exception as e:
        print(f"Erro: {e}")
        conexao.rollback()

    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    lista_pacientes()