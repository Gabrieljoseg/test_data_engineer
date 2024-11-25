from modules.database_manager import DatabaseManager
from modules.file_manager import FileManager
from modules.query_manager import QueryManager
import sys
import os

def setup_database(db_manager):
    """Configura o banco de dados inicial"""
    try:
        db_manager.create_database()
        return True
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")
        return False

def handle_file_operations(file_manager, download_url, zip_file, extract_folder):
    """Gerencia operações de arquivo com tratamento de erros"""
    try:
        # Primeiro, diagnosticar a URL
        print("\nDiagnosticando URL de download...")
        if not file_manager.diagnose_download(download_url):
            print("Diagnóstico falhou. Verifique a URL e as permissões do SharePoint.")
            return False

        # Se o arquivo já existe, removê-lo
        if os.path.exists(zip_file):
            os.remove(zip_file)
            print(f"Arquivo existente {zip_file} removido.")

        # Tentar download
        print("\nIniciando download do arquivo...")
        file_manager.download_file(download_url, zip_file)

        # Verificar se a pasta de extração existe
        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)
            print(f"Pasta de extração {extract_folder} criada.")

        # Extrair arquivo
        print("\nExtraindo arquivo...")
        file_manager.extract_zip(zip_file, extract_folder)
        
        return True
    except Exception as e:
        print(f"\nErro durante operações de arquivo: {e}")
        return False

def process_queries(query_manager):
    """Executa todas as queries necessárias"""
    try:
        # Criação das tabelas de pacientes
        print("\nCriando tabelas de pacientes...")
        query_manager.create_paciente_tables()
        
        # Inserção de dados de exemplo
        print("\nInserindo dados de exemplo...")
        query_manager.create_sample_hospital_data()
        
        # Cópia e análise dos dados
        print("\nProcessando dados de pacientes...")
        query_manager.copy_paciente_data()
        query_manager.find_duplicates()
        query_manager.select_most_recent()

        # Importação de dados meteorológicos
        print("\nImportando dados meteorológicos...")
        query_manager.import_weather_data()

        # Criação e população das tabelas de atendimento
        print("\nCriando tabelas de atendimento e exames...")
        query_manager.create_atendimento_exames_tables()

        # Análises
        print("\nRealizando análises...")
        query_manager.average_medications_prescribed()
                # Exemplos de uso para o Problema 9:
        query_manager.validate_prescription("aba", "cbaa")  # True
        query_manager.validate_prescription("aa", "b")  # False
        query_manager.validate_prescription("aa", "aab")  # True
        query_manager.validate_prescription("a", "b")  # False
        query_manager.visualize_attendances(["2024-11-23", "2024-11-23", "2024-11-22"])

        return True
    except Exception as e:
        print(f"\nErro durante processamento de queries: {e}")
        return False

def main():
    try:
        # Configurações
        database_name = "healthcare.db"
        download_url = "https://extremedigital-my.sharepoint.com/:u:/g/personal/david_duarte_extreme_digital/EZGUUGLnvChHs70A4VWpgpMBQdAjP1SX3AOxTcwbWzRafA?download=1"
        zip_file = "sigtap_data.zip"
        extract_folder = "data"

        # Instâncias das classes
        print("\nInicializando gerenciadores...")
        db_manager = DatabaseManager(database_name)
        file_manager = FileManager()
        query_manager = QueryManager(db_manager)

        # Executar etapas principais com verificação de erro
        if not setup_database(db_manager):
            sys.exit(1)

        if not handle_file_operations(file_manager, download_url, zip_file, extract_folder):
            sys.exit(1)

        print("\nInserindo arquivos no banco de dados...")
        db_manager.insert_files_into_db(extract_folder)

        if not process_queries(query_manager):
            sys.exit(1)

        print("\nProcessamento concluído com sucesso!")

    except Exception as e:
        print(f"\nErro crítico durante a execução: {e}")
        sys.exit(1)
    finally:
        # Limpeza opcional dos arquivos temporários
        if os.path.exists(zip_file):
            os.remove(zip_file)
            print(f"\nArquivo temporário {zip_file} removido.")

if __name__ == "__main__":
    main()