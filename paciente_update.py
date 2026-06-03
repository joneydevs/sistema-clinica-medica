from database import abrir_conexao
from queries import BUSCAR_PACIENTE_POR_ID, UPDATE_PACIENTE_POR_ID
from paciente_buscar import buscar
import psycopg2


def ajustar():
    conexao = abrir_conexao()
    if not conexao:
        return

    try:
        
        cursor = conexao.cursor()

        resultado_busca = buscar(cursor)

        if not resultado_busca:
            return
        
        mapa_pacientes = {str(p[0]): p for p in resultado_busca}

      
        id_digitado = input("Digite o id que precisa de ajuste: ").strip()

        if not id_digitado.isdigit():
            print("ERRO: O ID deve ser composto por número inteiros!")
            return
        
        if id_digitado not in mapa_pacientes:
            print("ERRO: O ID digitado deve estar entre os pacientes listados acima!")
            return

        id_a_ajustar = int(id_digitado)

        paciente_atual = mapa_pacientes[id_digitado]
        nome_antigo = paciente_atual[1]


        print (f"O registro atual a ser mudado será- ID:{paciente_atual[0]} | {paciente_atual[1]} | {paciente_atual[2]} | {paciente_atual[3]} ")
        
        confirmar = input("Deseja prosseguir? (Responda com: Sim ou Não)").lower()

        if confirmar != "sim":
            print ("Ok, update cancelado!")
            return
        

        while True:

            ajustar_nome = input("Digite nome correto: ").title().strip()
            ajustar_email = input ("Digite o e-mail correto: ").lower().strip()
            ajustar_celular = input ("Digite o celular correto: ").strip()

            if not id_a_ajustar or not ajustar_nome or not ajustar_email or not ajustar_celular:
                ajustes = input("Favor colocar um id, nome, email e celular para prosseguir ou 'sair' para finalizar.").strip().lower()

                if ajustes == "sair":
                    print ("Ok, operação cancelada!")
                    return

                else:
                    continue
            
            
            break
        
        cursor.execute(UPDATE_PACIENTE_POR_ID,(ajustar_nome, ajustar_email, ajustar_celular, id_a_ajustar,))
        conexao.commit()

        print (f"O nome '{ajustar_nome}' foi corrigido! e ficou assim:")
        cursor.execute(BUSCAR_PACIENTE_POR_ID,(id_digitado,))
        resultado_final = cursor.fetchone()

        if resultado_final:
            print (f"{resultado_final[0]} | {resultado_final[1]} | {resultado_final[2]} ")
            return

    except Exception as e:
        print (f"O processo falhou pelo erro: {e}!")
        conexao.rollback()
       
    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    ajustar()