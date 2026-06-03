from database import abrir_conexao
from medico_buscar import buscar_medico
from queries import UPDATE_PROFISSIONAL_POR_ID, BUSCAR_PROFISSIONAL_POR_ID
import psycopg2

def update():
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:
            
        cursor = conexao.cursor()

        resultado_buscar = buscar_medico(cursor)

        if not resultado_buscar:
            return
        
        mapa_medicos = {str(m[0]): m for m in resultado_buscar}
                        
        id_digitado = input("Digite o id do médico que precisa de ajuste: ").strip()

        if not id_digitado.isdigit():
            print("ERRO: O ID deve ser composto por número inteiros!")
            return

        if id_digitado not in mapa_medicos:
            print("ERRO: O ID digitado deve estar entre os médicos listados acima!")
            return

        id_ajustar = int(id_digitado)

        medico_atual = mapa_medicos[id_digitado]
        nome_antigo = medico_atual[1]
 

        print (f"O registro a ser mudado é ID: {medico_atual[0]}, especialista em {medico_atual[1]}, com email {medico_atual[2]} e celular {medico_atual[3]}?")
        
        confirma = input(f"Deseja prosseguir com o ajuste dos dados do médico {medico_atual[0]}? (sim/não)").lower().strip()

        if confirma != "sim":
            print ("Ok! Update cancelado!")
            return

        while True:
        
            nome = input("Digite o novo nome: ").title().strip()
            especialidade = input("Preencha a especialidade correta: ").title().strip()
            email = input("Preencha o email correto: ").lower()
            celular = input("Preencha o celular: ")

            if not nome or not especialidade or not email or not celular:
                ajustes = input("Favor colocar um nome, especialidade, email e celular para prosseguir ou 'sair' para finalizar.").strip().lower()

                if ajustes == "sair":
                    print ("Ok! Update cancelado!")
                    return
                
                else:
                    continue
                    
            break

        cursor.execute(UPDATE_PROFISSIONAL_POR_ID,(nome, especialidade, email, celular, id_ajustar,))
        conexao.commit()

        print(f"O médico {nome_antigo} foi atualizado com sucesso e ficou assim:")
        cursor.execute(BUSCAR_PROFISSIONAL_POR_ID, (id_ajustar,))
        resultado_final = cursor.fetchone()

        if resultado_final:
            print (f"{resultado_final[1]} | {resultado_final[2]} | {resultado_final[3]} | {resultado_final[4]}")
            return  

    except Exception as e:
        print (f"Erro de conexão: {e}")
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()



if __name__ == "__main__":
    update()