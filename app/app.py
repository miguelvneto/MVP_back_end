from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
import psycopg2

app = Flask(__name__)
CORS(app)

# Configuração do Swagger
swagger_url = '/swagger'
api_url = '/api/docs/swagger.json'

# Rota para a documentação do Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, config={'app_name': 'API de Atividades'})
app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

atividades = []

nome_tabela = "registro_manutencao"

def cursor_DB():
    # Conexão com o banco de dados
    conn = psycopg2.connect(
        dbname="servicelog",
        user="postgres",
        password="123",
        host="localhost"
    )
    cur = conn.cursor()
    
    return conn, cur

# Define a rota para cadastro de atividade
@app.route('/cadastrar_atividade', methods=['POST'])
def cadastrar_atividade():
    """Cadastra uma nova atividade"""
    json = request.get_json()

    # Verifica se todos os parâmetros obrigatórios foram enviados
    data = json.get("data")
    atividade = json.get("atividade")
    autor = json.get("autor")
    
    if data is None or atividade is None or autor is None:
        return 'Os campos "data", "atividade" e "autor" devem ser preenchidos.'
    
    # Conecta DB e cria um cursor
    conn, cur = cursor_DB()
    
    # Define os valores para a nova linha
    data = json["data"]
    atividade = json["atividade"]
    autor = json["autor"]

    # Inserção na tabela
    cur.execute('INSERT INTO '+nome_tabela+' (data, atividade, autor) VALUES (%s, %s, %s)', (data, atividade, autor))

    # Confirma as alterações no banco de dados
    conn.commit()

    # Fecha o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    return jsonify()

# Define a rota para listar atividade
@app.route('/listar_atividade', methods=['GET'])
def listar_atividade():
    """Lista as atividades"""
    # Conecta DB e cria um cursor
    conn, cur = cursor_DB()

    # Define o número de linhas que você deseja recuperar
    x = 10

    # Executa a consulta SQL para obter as últimas x linhas da tabela
    query = f'SELECT * FROM "'+nome_tabela+f'" ORDER BY id DESC LIMIT {x};'
    cur.execute(query)

    # Obtém os resultados da consulta
    rows = cur.fetchall()

    # Fecha o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    lista = []
    for atv in rows:
        lista.append({
            "id": atv[0],
            "data": atv[1].strftime("%Y/%m/%d"),
            "atividade": atv[2],
            "autor": atv[3]
        })
    return {'atividades': lista}

def retorna_atividade(atv):
    return {
        "id": atv[0],
        "data": atv[1],
        "atividade": atv[2],
        "autor": atv[3]
    }

# Define a rota para deletar atividade
@app.route('/deletar_atividade/<string:atividade>', methods=['DELETE'])
def deletar_atividade(atividade):
    """Deleta uma atividade pelo ID"""
    print(atividade)
    
    if atividade is None:
        return jsonify({'error': 'Atividade não encontrada.'}), 404
    
    # Conecta DB e cria um cursor
    conn, cur = cursor_DB()

    query = f'SELECT * FROM "'+nome_tabela+f'" where "id" = {atividade};'     
    cur.execute(query)
    conn.commit() 

    # Obtém os resultados da consulta
    if len(cur.fetchall()) == 0:

        # Fecha o cursor e a conexão com o banco de dados
        cur.close()
        conn.close()

        return jsonify({'message': 'Atividade Inexistente!'})

    query = f'DELETE FROM "'+nome_tabela+f'" where "id" = {atividade};'
    cur.execute(query)
    conn.commit() 

    # Fecha o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    return jsonify({'message': 'Atividade removida com sucesso!'}) 

@app.route('/api/docs/swagger.json', methods=['GET'])
def create_swagger_spec():
    """Gera a especificação do Swagger"""
    swag = swagger(app)
    swag['info']['version'] = '1.0.0'
    swag['info']['title'] = 'API de Atividades'
    swag['paths'] = {
        '/cadastrar_atividade': {
            'post': {
                'summary': 'Cadastra uma nova atividade',
                'responses': {
                    '200': {
                        'description': 'Atividade cadastrada com sucesso'
                    }
                }
            }
        },
        '/listar_atividade': {
            'get': {
                'summary': 'Lista as atividades',
                'responses': {
                    '200': {
                        'description': 'Lista de atividades'
                    }
                }
            }
        },
        '/deletar_atividade/{atividade}': {
            'delete': {
                'summary': 'Deleta uma atividade pelo ID',
                'parameters': [
                    {
                        'name': 'atividade',
                        'in': 'path',
                        'description': 'ID da atividade a ser deletada',
                        'required': True,
                        'schema': {
                            'type': 'string'
                        }
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'Atividade removida com sucesso'
                    },
                    '404': {
                        'description': 'Atividade não encontrada'
                    }
                }
            }
        }
    }
    return jsonify(swag)

if __name__ == '__main__':
    app.run()
