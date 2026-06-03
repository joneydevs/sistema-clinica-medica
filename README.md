# Sistema de Clínica Médica (Python CLI & PostgreSQL)

Este projeto consiste em um sistema completo de gerenciamento de clínica médica executado via Interface de Linha de Comando (CLI). O foco principal do desenvolvimento foi aplicar boas práticas de arquitetura de software, separação de conceitos (separation of concerns) e segurança da informação.

## Tecnologias Utilizadas

* **Python 3.12+**: Linguagem principal para orquestração e lógica de negócios.
* **PostgreSQL**: Banco de dados relacional para persistência dos dados de pacientes, médicos e agendamentos.
* **Docker**: Encapsulamento e execução do servidor de banco de dados em ambiente isolado.
* **Psycopg2**: Driver de conexão robusto entre a aplicação Python e o ecossistema Postgres.
* **Python-Dotenv**: Gerenciamento seguro de credenciais sensíveis por meio de variáveis de ambiente (`.env`).

## Diferenciais Arquiteturais do Projeto

* **Arquitetura Modular**: O sistema foi quebrado em submódulos independentes para operações de CRUD (Create, Read, Update, Delete), facilitando a manutenção e a escalabilidade do código.
* **Segurança (Zero Hardcoded Credentials)**: Nenhuma senha ou credencial de banco de dados foi exposta no código-fonte. O sistema consome variáveis de ambiente dinamicamente, seguindo padrões de produção.
* **Gerenciamento de Conexões**: Funções dedicadas para abertura e fechamento de conexões e cursores, evitando vazamento de memória (connection leaks) no banco de dados.
* **Interface Fluida**: Uso de rotinas de limpeza de terminal (`os.system`) para simular a experiência de um software de janela de forma leve e performática.
* **Regras de UX**: Adoção de práticas de UX, melhorando a experiência do usuário, como listagem de nomes, busca de identificadores, confirmação e reconfirmação de ações, sinalização de erros e recomendação de ações.

## Melhorias em andamento

Esse projeto prevê melhorias que serão adotadas a medida que os estudos forem evoluindo:

- Entendimento e uso de API;
- Sistema em WEB, além do CLI;
- Evolução na melhoria de regras de UX.
