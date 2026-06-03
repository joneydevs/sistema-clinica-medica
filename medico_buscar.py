from database import abrir_conexao
from queries import BUSCAR_MEDICO_POR_NOME
import psycopg2

def buscar_medico(cursor):
   
    try:
        medico_procurado = input("Digite o nome do médico que quer procurar: ").strip()
        cursor.execute(BUSCAR_MEDICO_POR_NOME,(medico_procurado + "%",))
        resultado = cursor.fetchall()

        print("\n"+"-"*15+" Resultado da Busca "+"-"*15+"\n")
        
        if resultado:
            for i in resultado:
                print (f"ID: {i[0]:<4} | Nome: {i[1]:<20}| Especialidade: {i[2]}!")

        else:
            print (f"O médico {medico_procurado} não está no cadastro!")

        return resultado

    except Exception as e:
        print(f"Erro de conexão: {e}")
        return []

if __name__ == "__main__":
    conexao = abrir_conexao()
    if conexao:
        cursor = conexao.cursor()
        buscar_medico(cursor)
        cursor.close()
        conexao.close()