from database import abrir_conexao
from queries import INSERIR_PACIENTE
import psycopg2

def cadastrar():
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:

        cursor = conexao.cursor()

        print("--- Cadastro de Novo Paciente ---")
        nome_novo = input("Digite o nome completo: ").strip().title()
        email_novo = input("Digite o e-mail (ex.: joney@yahoo.com.br): ").strip().lower()
        celular_novo = input("Digite o celular (ex.: 31999999996): ").strip()
   
        if not nome_novo or not email_novo or not celular_novo:
            print (" - Erro: Necessário incluir, nome, e-mail e celular obrigatoriamente!")
        
            return
        
        
        cursor.execute(INSERIR_PACIENTE, (nome_novo, email_novo, celular_novo))
        conexao.commit()

        print(f"\n Sucesso! '{nome_novo}', {email_novo}, {celular_novo} foram inseridos na base.")

    except Exception as e:
        print(f"\n Erro ao cadastrar: {e}")
        conexao.rollback()
            
    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    cadastrar()