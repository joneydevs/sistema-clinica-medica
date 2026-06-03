from database import abrir_conexao
from queries import BUSCAR_PACIENTE_POR_NOME, DELETAR_PACIENTE_POR_ID
import psycopg2

def deletar():
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:

        cursor = conexao.cursor()    

        while True:
            nome_deletar = input("Digite as primeiras letras do nome do paciente que deseja buscar: ").strip().lower()
            cursor.execute(BUSCAR_PACIENTE_POR_NOME,(nome_deletar + "%",))
            resultado = cursor.fetchall()

            if not resultado:

                print("Nenhum paciente encontrado na base!")
                opcao = input("Deseja procurar outro paciente? (sim/não)").strip().lower()
                if opcao != "sim":
                    print ("Ok, o cancelamento foi interrompido")
                    return
                else:
                    print("Vamos buscar outro nome!")
                    continue
            
            
            print("\n"+"-"*30+"PACIENTES NO BANCO"+"-"*30+"\n")
            for pac in resultado:
                print(f"ID: {pac[0]:<4} | NOME: {pac[1]:<20} | CELULAR: {pac[2]} | ")

            mapa_pacientes = {str(paci[0]): paci for paci in resultado}

        

            id_deletar = input("Digite o id do paciente que deseja deletar, ou (buscar) para procurar outro paciente: ").strip().lower()

            if id_deletar == "buscar":
                continue

            if id_deletar not in mapa_pacientes:
                print("ID digitado não pertence a um paciente cadastrado, favor refazer a busca!")
                continue

            break
        
        paciente_escolhido = mapa_pacientes[id_deletar]
        nome_paciente = paciente_escolhido[1]

        confirmar = input (f"Deseja prosseguir e deletar o paciente {nome_paciente}? (Escreva SIM/NÃO)").lower().strip()
        if confirmar != "sim":
            print ("Ok, o registro não será apagado")
            return

        confirmar2 = input ("TEM CERTEZA???? (Escreva SIM/NÃO)").lower().strip()
        if confirmar2 != "sim":
            print("Ok, o registro permanece!")
            return


        

        cursor.execute(DELETAR_PACIENTE_POR_ID,(id_deletar,))
        conexao.commit()

        print (f"O paciente {nome_paciente} foi deletado!")
        
    except Exception as e:
        print (f"O erro foi econtrado: {e} !")
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    deletar()