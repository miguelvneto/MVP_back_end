import psycopg2

# Estabelecer a conexão com o PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="localhost"
)

conn.autocommit = True

# Criar um cursor
cursor = conn.cursor()

# Criar o banco de dados "servicelog"
cursor.execute("CREATE DATABASE servicelog")

# Fechar a conexão atual
conn.close()

# Estabelecer uma nova conexão com o banco de dados "servicelog"
conn = psycopg2.connect(
    dbname="servicelog",
    user="postgres",
    password="123",
    host="localhost"
)

# Criar a tabela "registro_manutencao"
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE registro_manutencao (
        id SERIAL PRIMARY KEY,
        data DATE,
        atividade TEXT,
        autor TEXT
    )
""")

# Confirmar as alterações no banco de dados
conn.commit()

# Fechar a conexão e o cursor
cursor.close()
conn.close()

print("Banco de dados e tabela criados com sucesso!")
