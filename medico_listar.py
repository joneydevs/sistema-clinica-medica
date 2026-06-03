from database import abrir_conexao
from queries import LISTAR_MEDICOS
import psycopg2

def lista_medicos():
    conexao = abrir_conexao()
    if not conexao:
        return

    try:
    
        cursor = conexao.cursor()
        cursor.execute(LISTAR_MEDICOS)
        profissional = cursor.fetchall()

        print("\n"+"="*100)
        print("                                     MÉDICOS NO BANCO")
        print("="*100)
        
        for p in profissional:
            print(f"Esse é o ID: {p[0]:<4} | Nome: {p[1]:<25} | Especialidade: {p[2]:<15} | Email: {p[3]:<20}  | Celular {p[4]} ")

        
    except Exception as e:
        print(f"Erro: {e}")
        conexao.rollback()
    
    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    lista_medicos()