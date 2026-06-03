import os
from consulta_cadastrar import cadastrar as cadastrar_consultas
from consulta_deletar import deletar as cancelar_consultas
from consulta_listar import lista_consultas as listar_todas_consultas
from medico_buscar import buscar_medico as buscar_medicos
from medico_cadastrar import cadastrar as cadastrar_medicos
from medico_deletar import delete as deletar_medico
from medico_listar import lista_medicos as listar_todos_medicos
from medico_update import update as update_medicos
from paciente_buscar import buscar as buscar_pacientes
from paciente_cadastrar import cadastrar as cadastrar_pacientes
from paciente_deletar import deletar as deletar_paciente
from paciente_listar import lista_pacientes as listar_todos_pacientes
from paciente_update import ajustar as update_pacientes
from database import abrir_conexao
import psycopg2

# ==========================================
# 2. DESENHANDO O MENU
# ==========================================
def exibir_menu():
    print("=" * 50)
    print("             🏥 SISTEMA CLÍNICA MÉDICA")
    print("=" * 50)
    print("[ PACIENTES ]")
    print("1. Cadastrar Novo Paciente")
    print("2. Buscar Paciente")
    print("2.1 Listar todos os pacientes")
    print("3. Atualizar Dados do Paciente")
    print("4. Excluir Paciente\n")
    
    print("[ MÉDICOS ]")
    print("5. Cadastrar Novo Médico")
    print("6. Buscar Médico")
    print("7. Atualizar Dados do Médico")
    print("8. Excluir Médico\n")
    
    print("[ AGENDAMENTOS ]")
    print("9.  Marcar Nova Consulta")
    print("10. Listar Todas as Consultas")
    print("11. Cancelar Consulta\n")
    
    print("[ SISTEMA ]")
    print("0. Sair do Sistema")
    print("=" * 50)
# ==========================================
# 3. O CORAÇÃO DO SISTEMA (LOOP INFINITO)
# ==========================================
def main():
    while True:
        # Limpa a tela do terminal
        os.system('clear' if os.name == 'posix' else 'cls') 
        
        exibir_menu()
        
        opcao = input("\n➡️ Digite a opção desejada: ").strip()

        # ==========================================
        # --- AÇÕES DE PACIENTES ---
        # ==========================================
        if opcao == "1":
            print("\n>> Abrindo Cadastro de Paciente...\n")
            cadastrar_pacientes()
            input("\nPressione [ENTER] para voltar ao menu principal...")
            
        elif opcao == "2":
            print("\n>> Abrindo Busca de Paciente...\n")
            conexao = abrir_conexao()
            if conexao:
                cursor = conexao.cursor()
                buscar_pacientes(cursor)  # Entregamos o cursor para a função trabalhar!
                cursor.close()
                conexao.close()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        elif opcao =="2.1":
            print("\n Abrindo listagem completa dos pacientes...\n")
            listar_todos_pacientes()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        elif opcao == "3":
            print("\n>> Abrindo Atualização de Paciente...\n")
            update_pacientes()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        elif opcao == "4":
            print("\n>> Abrindo Exclusão de Paciente...\n")
            deletar_paciente()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        # ==========================================
        # --- AÇÕES DE MÉDICOS ---
        # ==========================================
        elif opcao == "5":
            print("\n>> Abrindo Cadastro de Médico...\n")
            cadastrar_medicos()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        elif opcao == "6":
            print("\n>> Abrindo Busca de Médico...\n")
            conexao = abrir_conexao()
            if conexao:
                cursor = conexao.cursor()
                buscar_medicos(cursor) # Entregamos o cursor para a função trabalhar!
                cursor.close()
                conexao.close()
            input("\nPressione [ENTER] para voltar ao menu principal...")
            
        elif opcao == "7":
            print("\n>> Abrindo Atualização de Médico...\n")
            update_medicos()
            input("\nPressione [ENTER] para voltar ao menu principal...")
            
        elif opcao == "8":
            print("\n>> Abrindo Exclusão de Médico...\n")
            deletar_medico()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        # ==========================================
        # --- AÇÕES DE AGENDAMENTO ---
        # ==========================================
        elif opcao == "9":
            print("\n>> Abrindo Marcação de Consulta...\n")
            cadastrar_consultas()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        elif opcao == "10":
            print("\n>> Abrindo Lista de Consultas...\n")
            listar_todas_consultas()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        elif opcao == "11":
            print("\n>> Abrindo Cancelamento de Consulta...\n")
            cancelar_consultas()
            input("\nPressione [ENTER] para voltar ao menu principal...")

        # ==========================================
        # --- SAÍDA ---
        # ==========================================
        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo! 👋\n")
            break # Quebra o loop e desliga o programa
            
        else:
            print("\n❌ Opção inválida! Tente digitar um número do menu.")
            input("\nPressione [ENTER] para voltar ao menu...")

# ==========================================
# 4. LIGANDO O INTERRUPTOR
# ==========================================
if __name__ == "__main__":
    main()