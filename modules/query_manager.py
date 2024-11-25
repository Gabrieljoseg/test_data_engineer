import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import requests

class QueryManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_paciente_tables(self):
        """Cria todas as tabelas de pacientes necessárias"""
        tables = [
            'paciente_prontuario',
            'paciente_hospital_a',
            'paciente_hospital_b',
            'paciente_hospital_c'
        ]
        
        for table in tables:
            query = f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                dt_nascimento DATE,
                cpf TEXT,
                nome_mae TEXT,
                dt_atualizacao TIMESTAMP
            );
            """
            self.db_manager.execute_query(query, f"Tabela {table} criada com sucesso.")

    def create_sample_hospital_data(self):
        """Cria dados de exemplo para os hospitais"""
        hospitals = ['paciente_hospital_a', 'paciente_hospital_b', 'paciente_hospital_c']
        
        sample_data = [
            ('João Silva', '1990-01-01', '12345678901', 'Maria Silva', '2023-01-01'),
            ('Ana Santos', '1985-05-15', '98765432101', 'Julia Santos', '2023-02-01'),
            ('Carlos Oliveira', '1978-08-20', '12345678901', 'Teresa Oliveira', '2023-03-01')
        ]
        
        for hospital in hospitals:
            insert_query = f"""
            INSERT OR IGNORE INTO {hospital} 
                (nome, dt_nascimento, cpf, nome_mae, dt_atualizacao)
            VALUES 
                (?, ?, ?, ?, ?);
            """
            try:
                conn = sqlite3.connect(self.db_manager.db_name)
                cursor = conn.cursor()
                cursor.executemany(insert_query, sample_data)
                conn.commit()
                print(f"Dados de exemplo inseridos em {hospital}")
            except Exception as e:
                print(f"Erro ao inserir dados em {hospital}: {e}")
            finally:
                conn.close()

    def copy_paciente_data(self):
        """Copia dados dos hospitais para a tabela consolidada"""
        query = """
        INSERT OR REPLACE INTO paciente_prontuario 
            (nome, dt_nascimento, cpf, nome_mae, dt_atualizacao)
        SELECT nome, dt_nascimento, cpf, nome_mae, dt_atualizacao
        FROM paciente_hospital_a
        UNION ALL
        SELECT nome, dt_nascimento, cpf, nome_mae, dt_atualizacao
        FROM paciente_hospital_b
        UNION ALL
        SELECT nome, dt_nascimento, cpf, nome_mae, dt_atualizacao
        FROM paciente_hospital_c;
        """
        self.db_manager.execute_query(query, "Dados copiados para a tabela consolidada.")

    def find_duplicates(self):
        """Encontra registros duplicados baseados no CPF"""
        query = """
        SELECT cpf, COUNT(*) AS quantidade
        FROM paciente_prontuario
        GROUP BY cpf
        HAVING quantidade > 1;
        """
        duplicates = self.db_manager.fetch_query(query)
        print("Pacientes duplicados:", duplicates)

    def select_most_recent(self):
        """Seleciona os registros mais recentes para cada CPF"""
        query = """
        SELECT id, nome, dt_nascimento, cpf, nome_mae, dt_atualizacao
        FROM paciente_prontuario p1
        WHERE dt_atualizacao = (
            SELECT MAX(dt_atualizacao)
            FROM paciente_prontuario p2
            WHERE p1.cpf = p2.cpf
        );
        """
        most_recent = self.db_manager.fetch_query(query)
        print("Registros mais recentes:", most_recent)

    def import_weather_data(self):
        """Importa dados meteorológicos da API Open Meteo"""
        try:
            url = "https://api.open-meteo.com/v1/forecast?latitude=-22.9068&longitude=-43.1729&hourly=pressure_msl"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            # Criar DataFrame com os dados
            df = pd.DataFrame({
                'momento': data['hourly']['time'],
                'valor': data['hourly']['pressure_msl']
            })

            # Conectar ao banco e salvar os dados
            conn = sqlite3.connect(self.db_manager.db_name)
            df.to_sql('previsao_pressao_atm', conn, if_exists='replace', index=False)
            conn.close()
            print("Dados meteorológicos importados com sucesso.")
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API meteorológica: {e}")
        except Exception as e:
            print(f"Erro ao importar dados meteorológicos: {e}")

    def create_atendimento_exames_tables(self):
        """Cria as tabelas de atendimento e exames"""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS atendimento (
                id INTEGER PRIMARY KEY,
                tp_atend TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS atendimento_exame (
                id INTEGER PRIMARY KEY,
                id_atendimento INTEGER,
                exame TEXT,
                FOREIGN KEY (id_atendimento) REFERENCES atendimento(id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS atendimento_prescricao (
                id INTEGER PRIMARY KEY,
                id_atend INTEGER,
                medicamento TEXT,
                FOREIGN KEY (id_atend) REFERENCES atendimento(id)
            );
            """
        ]
        
        for query in queries:
            self.db_manager.execute_query(query)

        # Inserir dados de exemplo
        sample_data = [
            """
            INSERT OR IGNORE INTO atendimento (id, tp_atend) VALUES 
                (1, 'U'), (2, 'U'), (3, 'N');
            """,
            """
            INSERT OR IGNORE INTO atendimento_prescricao (id_atend, medicamento) VALUES
                (1, 'Dipirona'), (1, 'Paracetamol'),
                (2, 'Ibuprofeno'), (2, 'Amoxicilina'), (2, 'Dipirona');
            """
        ]
        
        for query in sample_data:
            self.db_manager.execute_query(query)

    def average_medications_prescribed(self):
        """Calcula a média de medicamentos prescritos"""
        query = """
        SELECT ROUND(AVG(quantidade), 2) AS media
        FROM (
            SELECT id_atend, COUNT(*) AS quantidade
            FROM atendimento_prescricao
            WHERE id_atend IN (
                SELECT id
                FROM atendimento
                WHERE tp_atend = 'U'
            )
            GROUP BY id_atend
        );
        """
        result = self.db_manager.fetch_query(query)
        if result is not None and not result.empty:
            print(f"Média de medicamentos prescritos: {result['media'].iloc[0]}")
        else:
            print("Não há dados de prescrição disponíveis.")

    def validate_prescription(self, prescription, stock):
        """Valida se uma prescrição pode ser atendida com o estoque disponível"""
        prescription_count = {char: prescription.count(char) for char in set(prescription)}
        stock_count = {char: stock.count(char) for char in set(stock)}
        is_valid = all(stock_count.get(key, 0) >= value for key, value in prescription_count.items())
        print(f"Prescrição válida: {is_valid}")

    def visualize_attendances(self, dates):
        """Visualiza atendimentos por dia"""
        attendance_counts = pd.Series(dates).value_counts()
        plt.figure(figsize=(10, 6))
        attendance_counts.plot(kind="bar", title="Atendimentos por Dia")
        plt.xlabel("Data")
        plt.ylabel("Quantidade de Atendimentos")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()