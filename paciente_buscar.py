from database import abrir_conexao
from queries import BUSCAR_PACIENTE_POR_NOME
import psycopg2

def buscar(cursor):

    try:
        nome_procurado = input("Digite o nome do paciente para buscar: ").strip()
        cursor.execute(BUSCAR_PACIENTE_POR_NOME, (nome_procurado + "%",))
        resultado = cursor.fetchall()

        print("\n"+"-"*35+" Resultado da Busca "+"-"*35+"\n")
        if resultado:
            for i in resultado:
                print(f"ID: {i[0]:<5} | Nome: {i[1]:<20} | Celular: {i[2]:<14} | Email: {i[3]}")
            print ("\n")
        else:
            print(f"O paciente '{nome_procurado}' não está no banco.")

        return resultado

    except Exception as e:
        print(f"Erro de conexão: {e}")
        return []
    
if __name__ == "__main__":
    conexao = abrir_conexao()
    if conexao:
        cursor = conexao.cursor()
        buscar(cursor)
        cursor.close()
        conexao.close()