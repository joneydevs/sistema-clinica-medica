from database import abrir_conexao
from queries import BUSCAR_CONSULTAS_POR_NOME_PACIENTE, UPDATE_CONSULTA_POR_ID
import psycopg2

def deletar():
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:
    
        cursor = conexao.cursor()

        consulta_deletar = input("Digite as primeiras letras do nome do paciente: ").strip()
        cursor.execute(BUSCAR_CONSULTAS_POR_NOME_PACIENTE,(consulta_deletar + "%",))
        resultado = cursor.fetchall()

        if not resultado:
            print("Nenhuma consulta encontrada para este paciente!")
            return

        mapa_consultas = {str(p[0]): p for p in resultado}

        print("\n" + "-"*30 + " CONSULTAS ENCONTRADAS " + "-"*30 + "\n")
        for p in resultado:
            data_br = p[4].strftime("%d/%m/%y %H:%M") if p[4] else p[4]
            print(f"ID: {p[0]:<3} | NOME: {p[1]:<20} | MÉDICO: {p[2]:<20} | {p[3]:<13} | DATA: {data_br} | STATUS: {p[5]:<8}")
        
        id_consulta_deletar = input("Digite o ID da consulta a deletar: ").strip()

        if id_consulta_deletar not in mapa_consultas:
            print("\n ID não está entre as consultas selecionadas, favor refazer a escolha!")
            return
        
        selecionada = mapa_consultas[id_consulta_deletar]

        data_selecionada = selecionada[4].strftime("%d/%m/%Y %H:%M") if selecionada[4] else selecionada[4]
        
       
        print("*"*50)
        print("        CONSULTA SELECIONADA")
        print("*"*50)
        print(f"MÉDICO: {selecionada[2]:<20}")
        print(f"DATA_HORA: {data_selecionada}")
        print(f"STATUS: {selecionada[5]}")

        if selecionada[5].strip().upper() == "CANCELADA":
            print("Consulta já tem status de cancelada!")
            return
            

        confirma_delete = input("\n Deseja cancelar a consulta? (sim/não)").lower().strip()

        if confirma_delete != "sim":
            print("Consulta permanece marcada!")
            return            
        
        cursor.execute(UPDATE_CONSULTA_POR_ID,(id_consulta_deletar,))
        conexao.commit()
    
        
        print(f"Consulta de {selecionada[1]:<10}, com o médico {selecionada[2]:<10}, foi cancelada!")
                  


    except Exception as e:
        print (f"Erro de conexão: {e}")
        conexao.rollback()

    finally:

        cursor.close()
        conexao.close()

        
if __name__ == "__main__":
    deletar()





