# Avaliação Data Engineer

## Introdução

Este projeto é uma aplicação em Python que gerencia informações de pacientes de forma organizada utilizando um banco de dados SQLite. Ele inclui funcionalidades para manipulação de dados, como a criação de tabelas, inserção de dados, e análise de informações. Além disso, a aplicação também importa dados meteorológicos de uma API externa e gerencia arquivos em formato ZIP.

## Estrutura do Projeto

O projeto é modularizado em várias classes, cada uma responsável por uma parte específica da funcionalidade. Abaixo está uma descrição das principais classes incluídas no código.

### Classes

1. **DatabaseManager**
   - Gerencia as operações do banco de dados SQLite.
   - Métodos:
     - `execute_query`: Executa uma query SQL e opcionalmente exibe uma mensagem de sucesso.
     - `fetch_query`: Retorna resultados de uma query SELECT.
     - `create_database`: Cria um banco de dados SQLite.
     - `insert_files_into_db`: Insere dados de arquivos em tabelas do banco de dados.
     - `list_tables`: Lista todas as tabelas presentes no banco de dados.

2. **FileManager**
   - Gerencia operações de download e extração de arquivos.
   - Métodos:
     - `download_file`: Faz o download de arquivos de uma URL, com tratamento de erros.
     - `extract_zip`: Extrai arquivos ZIP com validação.
     - `diagnose_download`: Diagnostica problemas com o download, retornando informações detalhadas.

3. **QueryManager**
   - Realiza operações específicas sobre os dados dos pacientes.
   - Métodos:
     - `create_paciente_tables`: Cria as tabelas necessárias para armazenar dados de pacientes.
     - `create_sample_hospital_data`: Insere dados de exemplo para hospitais.
     - `copy_paciente_data`: Copia dados de várias tabelas para uma tabela consolidada.
     - `find_duplicates`: Encontra registros duplicados com base no CPF.
     - `select_most_recent`: Seleciona os registros mais recentes para cada CPF.
     - `import_weather_data`: Importa dados meteorológicos de uma API.
     - `create_atendimento_exames_tables`: Cria tabelas para atendimentos e exames.
     - `average_medications_prescribed`: Calcula a média de medicamentos prescritos.
     - `validate_prescription`: Valida se uma prescrição pode ser atendida com o estoque disponível.
     - `visualize_attendances`: Visualiza a quantidade de atendimentos por dia.

### Funções Principais

- `setup_database`: Configura o banco de dados inicial.
- `handle_file_operations`: Gerencia as operações de download e extração de arquivos.
- `process_queries`: Executa uma série de queries necessárias para manipulação de dados de pacientes.

### Execução do Código

Para executar o código, siga os passos abaixo:

1. Certifique-se de que você tem o Python instalado na sua máquina. Você pode baixá-lo [aqui](https://www.python.org/downloads/).
2. Instale as bibliotecas necessárias:
   ```bash
   pip install pandas matplotlib requests
   ```
3. Execute o script principal. Você pode fazer isso em um terminal com o seguinte comando:
   ```bash
   python3 main.py
   ```

