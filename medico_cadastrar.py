from database import abrir_conexao
from queries import (INSERIR_PROFISSIONAL, BUSCAR_MEDICO_POR_NOME)

import psycopg2

def cadastrar():
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:

        cursor = conexao.cursor()
        
        print ("Tudo pronto para o cadastrado de novo médico")

        nome = input("Digite o nome do médico: ").title().strip()
        espec = input("Digite a especialidade do médico :").title().strip()
        email = input("Digite o email: ").strip()
        celular = input("Digite o celular: ").strip()
       
        if not nome or not espec or not email or not celular:
            print ("Por favor, recomece o cadastro e inclua todos os campos solicitados")
            return
        
        cursor.execute(INSERIR_PROFISSIONAL,(nome,espec,email,celular,))

        cursor.execute(BUSCAR_MEDICO_POR_NOME,(nome,))
        resultado = cursor.fetchone()

        if resultado:
            print (f"O médico {resultado[1]}, especialista em {resultado[2]}, email: {resultado[3]}, celular: {resultado[4]} será cadastrado!")
            
            confirmar = input("Confirma o cadastramento? (Digite Sim/Não)").lower().strip()

            if confirmar != "sim":
                print ("Cadastramento cancelado, recomece o cadastramento!")
                return

            else:

                print (f"O médico {resultado[1]}, especialista em {resultado[2]}, email: {resultado[3]}, celular: {resultado[4]} foi cadastrado!")    



        conexao.commit()

            
        

    except Exception as e:
        print (f"Infelizmente houve o erro: {e}")
        conexao.rollback()
        

    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    cadastrar()