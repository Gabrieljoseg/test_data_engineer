import os
import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, success_message=None):
        """Executa uma query no banco de dados."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            if success_message:
                print(success_message)
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
        finally:
            conn.close()

    def fetch_query(self, query):
        """Executa uma query de seleção e retorna os resultados."""
        try:
            conn = sqlite3.connect(self.db_name)
            result = pd.read_sql_query(query, conn)
            return result
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
        finally:
            conn.close()


    def create_database(self):
        """Cria o banco de dados SQLite."""
        conn = sqlite3.connect(self.db_name)
        conn.close()
        print(f"Banco de dados '{self.db_name}' criado com sucesso.")

    def insert_files_into_db(self, folder_path):
        """Insere os dados de arquivos em um banco de dados SQLite."""
        conn = sqlite3.connect(self.db_name)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            try:
                if file_name.endswith(".txt"):
                    data = pd.read_csv(file_path, sep="\t")
                elif file_name.endswith(".xls") or file_name.endswith(".xlsx"):
                    data = pd.read_excel(file_path)
                else:
                    continue

                # Inferir o nome da tabela pelo nome do arquivo
                table_name = os.path.splitext(file_name)[0]
                data.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Tabela '{table_name}' criada e preenchida com sucesso.")
            except Exception as e:
                print(f"Erro ao processar arquivo '{file_name}': {e}")
        conn.close()

    def list_tables(self):
        """Lista todas as tabelas no banco de dados."""
        conn = sqlite3.connect(self.db_name)
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(query, conn)
        conn.close()
        return tables
