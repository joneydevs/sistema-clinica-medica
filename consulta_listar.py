from database import abrir_conexao
from queries import LISTAR_CONSULTAS
import psycopg2

def lista_consultas():
    conexao = abrir_conexao()
    if not conexao:
        return

    try:
        
        cursor = conexao.cursor()
        cursor.execute(LISTAR_CONSULTAS)
        consultas = cursor.fetchall()
        
        print("\n"+"="*100)
        print("                                     CONSULTAS CADASTRADAS")
        print("="*100)
        
        for c in consultas:
            data_formatada = c[3].strftime("%d/%m/%y às %H:%M")
            print (f"ID: {c[0]:<4} | PACIENTE: {c[1]:<20} | MÉDICO: {c[2]:<20} | DATA: {data_formatada} | STATUS: {c[4]} ")


    except Exception as e:
        print (f"Erro: {e}")
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    lista_consultas()