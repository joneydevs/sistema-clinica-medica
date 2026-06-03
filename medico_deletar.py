from database import abrir_conexao
from queries import BUSCAR_MEDICO_POR_NOME, DELETAR_PROFISSIONAL_POR_ID
import psycopg2

def delete():
    conexao = abrir_conexao()
    if not conexao:
        return

    try:
        
        cursor = conexao.cursor()
        
        while True:
            nome_deletar = input("Digite as primeiras letras do nome do médico que deseja buscar: ").strip().lower()
            cursor.execute(BUSCAR_MEDICO_POR_NOME,(nome_deletar + "%",))
            resultado = cursor.fetchall()

            if not resultado:
                print("Nenhum médico encontrado na base!")
                opcao = input("Deseja procurar outro médico? (sim/não)").strip().lower()
                
                if opcao != "sim":
                    print ("Ok, o cancelamento foi interrompido")
                    return
                
                else:
                    print("Vamos buscar outro nome!")
                    continue

            print("\n"+"-"*30+"MÉDICOS NO BANCO"+"-"*30+"\n")
            for mec in resultado:
                print(f"ID: {mec[0]:<4} | NOME: {mec[1]:<20} | CELULAR: {mec[4]} | ")

            mapa_medicos = {str(meci[0]): meci for meci in resultado}

            id_deletar = input("Digite o id do médico que deseja deletar, ou (buscar) para procurar outro médico: ").strip().lower()

            if id_deletar == "buscar":
                continue

            if id_deletar not  in mapa_medicos:
                print("ID digitado não pertence a um médico cadastrado, favor refazer a busca!")
                continue

            break

        med_escolhido = mapa_medicos[id_deletar]
        nome_medico = med_escolhido[1]

        
         
        confirma = input (f"Deseja seguir com a exclusão do médico {nome_medico}? (Sim/Não)").lower().strip()
        if confirma != "sim":
            print ("Ok, o registro não será apagado")
            return
            
        confirma2 = input ("Tem certeza? Após essa confirmação a ação não poderá ser desfeita! (Sim/Não)").lower().strip()

        if confirma2 != "sim":
            print ("Ok, o registro não será deletado!")
            return
        
        
        cursor.execute(DELETAR_PROFISSIONAL_POR_ID,(id_deletar,))
        conexao.commit()

        print(f"O médico {med_escolhido[1]}, especialista em {med_escolhido[2]} foi excluído da base!")

    except Exception as e:
        print(f"Erro de conexão: {e}")
        conexao.rollback()
        

    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    delete()