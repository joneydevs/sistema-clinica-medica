from queries import (
    BUSCAR_PROFISSIONAIS_POR_ESPECIALIDADE,
    BUSCAR_DETALHES_PROFISSIONAL,
    VERIFICAR_OCUPACAO_MEDICO_30_DIAS,
    VERIFICAR_HORARIO_DISPONIVEL,
    BUSCAR_PACIENTES_POR_APROXIMACAO,
    INSERIR_CONSULTA,
    BUSCAR_RESUMO_AGENDAMENTO)

from database import abrir_conexao
import psycopg2 # Pacote que permite o entendimento entre o SELECT inserido no PYTHON pelo PostGres"
from psycopg2 import errors #submodulo que identifica os erros, no caso estou usando para violação de unicidade, pois no schema do banco não pode haver repetição de dia e hora para médico ou paciente
from datetime import datetime #Dateime é uma biblioteca nativa, já o submodulo datetime é um obejto permite o tramento de data e hora juntos
from datetime import timedelta #timedelta é um submodulo que permite a contagem do tempo, respeitando calendário 30/04 + 1 dia retorna como 01/05


def eh_dia_util(data_str):
    try:

        data_limpa = data_str.strip().replace("/", "-")

        data_obj = datetime.strptime(data_limpa, "%d-%m-%Y")
        return data_obj.weekday() < 5
    except ValueError:
        return None

def cadastrar():
    conexao = abrir_conexao()
    if not conexao:
        return

    try:
      
        cursor = conexao.cursor()

        while True:

            espec = input("Escreva as primeiras letras da especialidade. Ex.: Para otorrinolaringolista - Escreva Otorrino: ").title().strip()
            cursor.execute(BUSCAR_PROFISSIONAIS_POR_ESPECIALIDADE,(espec + "%",))
            resultado = cursor.fetchall()

            if not resultado:
                print("Nenhum médico disponível com essa especialidade, selecione novamente!")
                continue

            print("\n" + "*"*45)
            print("      LISTA DE MÉDICOS POR ESPECIALIDADE")
            print("*"*45)
            
            for medico in resultado:
                print(f"ID:{medico[0]:<5} | Dr(a). {medico[1]:<20} | {medico[2]}")
        
            
            id_validos = [str(medico[0]) for medico in resultado]
            horario_atendimento = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

            medico_escolhido = input(f"Digite o id do médico escolhido: ").strip()
            
            if medico_escolhido not in id_validos:
                print ("O ID escolhido não está entre os médicos listados, favor alterar a selecão!")
                continue
            
            break

        cursor.execute(BUSCAR_DETALHES_PROFISSIONAL,(medico_escolhido,))
        nome_medico = cursor.fetchone()

        cursor.execute(VERIFICAR_OCUPACAO_MEDICO_30_DIAS,(medico_escolhido,))
        ocupacao_por_dia = dict(cursor.fetchall())

        while True:
        
            print(f"\n--- DISPONIBILIDADE PARA OS PRÓXIMOS 30 DIAS DO MÉDICO {nome_medico[0]} | {nome_medico[1]} ---")
            print(f"{'DATA':<12} | {'STATUS'}")
            print("-" * 35)

            hoje = datetime.now()
            limite_vagas = len(horario_atendimento)

            for i in range(30):
                dia_analisado = hoje + timedelta(days=i)
                data_formatada = dia_analisado.date()

                if eh_dia_util(data_formatada.strftime("%d-%m-%Y")):
                    agendados = ocupacao_por_dia.get(data_formatada,0)
                    vagas_livres = limite_vagas - agendados

                    if vagas_livres > 0:
                        print(f"{data_formatada.strftime('%d/%m/%y')} ({(dia_analisado.strftime('%a'))}) | {vagas_livres} horários livres ")
                    else:
                        print(f"{data_formatada.strftime('%d/%m/%y')} ({(dia_analisado.strftime('%a'))}) | ESGOTADO ")
            print("-" * 35)

            data_escolhida = input("\nDigite a data escolhida (DD-MM-AAAA) ou 'sair': ").strip().lower()
            
            if data_escolhida == 'sair':
                return
            
            if not eh_dia_util(data_escolhida):
                print ("\nA data escolhida não é dia útil ou o formato está errado!")
                input("\nPressione [ENTER] para ver o calendário novamente...")
                continue

            break

        data_limpa = data_escolhida.strip().replace("/", "-")
        data_objeto = datetime.strptime(data_limpa, "%d-%m-%Y")
        data_banco = data_objeto.strftime("%Y-%m-%d")

        print(f"\n Horários livres para o dia {data_escolhida}:")
        print(", ".join(horario_atendimento))
        
        while True:
            hora_escolhida = input("\nDigite o horário da consulta (ex: 09:00): ").strip()
            if hora_escolhida not in horario_atendimento:
                print("Horário inválido, escolha um horário válido: ")
                print(f"Horários válidos : {horario_atendimento}")
                continue

            data_hora_final = f"{data_banco} {hora_escolhida}"
            cursor.execute(VERIFICAR_HORARIO_DISPONIVEL,(medico_escolhido, data_hora_final,))
            if cursor.fetchone():
                print(f"Horário escolhido não está disponível!")
            else:
                print ("Horário disponível")
                break


        print (data_hora_final)

        while True:

            paciente = input("Digite o nome do paciente para o qual deseja marcar consulta: (digitar as três primeiras letras do nome: Maria - Mar)").strip().lower()
            cursor.execute(BUSCAR_PACIENTES_POR_APROXIMACAO,(paciente + "%",))
            resultado2 = cursor.fetchall()

            if not resultado2:
                print("\n Nenhum paciente encontrado cujo nome inicia com primeiras letras do nome digitadas!")
                opcao = input("Deseja procurar outro paciente? (sim/não)").strip().lower()
                if opcao != "sim":
                    print ("Agendamento cancelado, faça o cadastro do paciente não econtrado!")
                    return
                else:
                    print("Vamos bucar outro nome!")
                    continue

            print ("\n"+"*"*45)
            print ("        LISTA DE PACIENTES CADASTRADOS")
            print ("*"*45)

            for pac in resultado2:
                print(f"ID: {pac[0]:<5} | NOME: {pac[1]:<20}")
                
               
            id_validos_paciente = [str(paciente[0]) for paciente in resultado2]
            paciente_selecionado = input("Digite o ID do paciente selecionado (ou digite 'buscar' para pesquisar outro nome): ").strip().lower()

            if paciente_selecionado == "buscar":
                continue

            if paciente_selecionado not in id_validos_paciente:
                print ("O ID escolhido não está entre os pacientes listados, favor alterar a selecão!")
                continue

            break
            
        cursor.execute(INSERIR_CONSULTA, (paciente_selecionado, medico_escolhido, data_hora_final),)

        cursor.execute(BUSCAR_RESUMO_AGENDAMENTO,(paciente_selecionado,medico_escolhido,data_hora_final,))
        res = cursor.fetchone()

        if res:
            nome_paciente = res[0]
            nome_medico = res[1]
            especialidade = res[2]

            print("\n" + "="*50)
            print("                  RESUMO AGENDAMENTO")        
            print("="*50)
            print(f"PACIENTE:       {nome_paciente}")
            print(f"MÉDICO:         {nome_medico}")
            print(f"ESPECIALIDADE:  {especialidade}")
            print(f"DATA_HORA:      {data_hora_final}")
            print("="*50)

            confirma = input(f"Confirma a consulta para os dados acima? (sim/não) ").lower()

            if confirma != "sim":
                print ("Agendamento cancelado")
                conexao.rollback()
                return
        
        conexao.commit()

        print(f"MARCAÇÃO CONCLUÍDA PARA {nome_paciente}, COM O MÉDICO {nome_medico}, em {data_hora_final}!")


    except errors.UniqueViolation as e:
        print ("="*50)
        print ("ATENÇÃO! CONFLITO DE AGENDA IMPEDINDO AGENDAMENTO!")
        print ("="*50+"\n")
        if "consulta_paciente_id_data_hora_key" in str(e):
            print ("PACIENTE JÁ TEM UMA CONSULTA AGENDADA PARA MESMO DIA E HORA!")
        elif "consulta_profissional_id_data_hora_key" in str(e):
            print ("MÉDICO JÁ POSSUI CONSULTA AGENDADA PARA MESMO DIA E HORA COM OUTRO PACIENTE!")
        print ("O AGENDAMENTO FOI CANCELADO ALTERE SUA ESCOLHA")
        print ("\n"+"="*50)
        conexao.rollback()


    except Exception as w:
        print(f"Erro de conexão: {w}")
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()


if __name__ == "__main__":
    cadastrar()