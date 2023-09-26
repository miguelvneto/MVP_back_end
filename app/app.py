from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from googletrans import Translator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mvp.db'
db = SQLAlchemy(app)
CORS(app)

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    atividade = db.Column(db.String(255))
    autor = db.Column(db.String(100))

# Configuração do Swagger
swagger_url = '/swagger'
api_url = '/api/docs/swagger.json'

# Rota para a documentação do Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(swagger_url, api_url, config={'app_name': 'API de Atividades'})
app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

atividades = []

nome_tabela = "registro_manutencao"

# Define a rota para cadastro de atividade
@app.route('/cadastrar_atividade', methods=['POST'])

def cadastrar_atividade():
    json = request.get_json()

    # Verifica se todos os parâmetros obrigatórios foram enviados
    data = json.get("data")
    atividade = json.get("atividade")
    autor = json.get("autor")

    if data is None or atividade is None or autor is None:
        return 'Os campos "data", "atividade" e "autor" devem ser preenchidos.'

    data_obj = datetime.strptime(data, "%Y-%m-%d").date()

    # Cria um novo registro no banco de dados usando o modelo
    nova_atividade = Atividade(data=data_obj, atividade=atividade, autor=autor)
    db.session.add(nova_atividade)
    db.session.commit()

    return jsonify({'message': 'Atividade cadastrada com sucesso'})

# Define a rota para duplicar uma atividade pelo ID
@app.route('/duplicar_atividade/<int:atividade_id>', methods=['POST'])
def duplicar_atividade(atividade_id):
    # Busca a atividade pelo ID
    atividade_original = Atividade.query.get(atividade_id)

    if atividade_original is None:
        return jsonify({'error': 'Atividade não encontrada.'}), 404

    # Cria uma cópia da atividade original, mantendo a mesma data, atividade e autor
    nova_atividade = Atividade(data=atividade_original.data, atividade=atividade_original.atividade, autor=atividade_original.autor)
    db.session.add(nova_atividade)
    db.session.commit()

    return jsonify({'message': 'Atividade duplicada com sucesso!'})

# Define a rota para listar atividade
@app.route('/listar_atividade', methods=['GET'])
def listar_atividade():
    """Lista as atividades"""
    # Consulta os últimos 10 registros da tabela Atividade
    atividades = Atividade.query.order_by(Atividade.id.desc()).limit(10).all()

    lista = []
    for atv in atividades:
        lista.append({
            "id": atv.id,
            "data": atv.data.strftime("%Y/%m/%d"),
            "atividade": atv.atividade,
            "autor": atv.autor
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
@app.route('/deletar_atividade/<string:atividade_id>', methods=['DELETE'])
def deletar_atividade(atividade_id):
    # Busca a atividade pelo ID
    atividade = Atividade.query.get(atividade_id)

    if atividade is None:
        return jsonify({'error': 'Atividade não encontrada.'}), 404

    # Remove a atividade do banco de dados
    db.session.delete(atividade)
    db.session.commit()

    return jsonify({'message': 'Atividade removida com sucesso!'})

# Define a rota para atualizar uma atividade pelo ID
@app.route('/atualizar_atividade/<int:atividade_id>', methods=['PUT'])
def atualizar_atividade(atividade_id):
    # Busca a atividade pelo ID
    atividade = Atividade.query.get(atividade_id)

    if atividade is None:
        return jsonify({'error': 'Atividade não encontrada.'}), 404

    # Obtém os dados do JSON da solicitação
    json = request.get_json()
    data = json.get("data")
    atividade_texto = json.get("atividade")
    autor = json.get("autor")

    if data is None or atividade_texto is None or autor is None:
        return 'Os campos "data", "atividade" e "autor" devem ser preenchidos.', 400

    data_obj = datetime.strptime(data, "%Y-%m-%d").date()

    # Atualiza os dados da atividade
    atividade.data = data_obj
    atividade.atividade = atividade_texto
    atividade.autor = autor

    # Commit das alterações no banco de dados
    db.session.commit()
 
    return jsonify({'message': 'Atividade atualizada com sucesso!'})

# Cria uma instância do tradutor do Google
translator = Translator()

# Define a rota para traduzir um texto
@app.route('/traduzir_texto', methods=['POST'])
def traduzir_texto():
    json = request.get_json()

    # Verifica se o parâmetro 'texto' foi enviado
    texto = json.get("texto")

    if texto is None:
        return 'O campo "texto" deve ser preenchido.'

    # Traduz o texto para um idioma de destino (por exemplo, inglês)
    destino = 'en'  # Altere o idioma de destino conforme necessário
    texto_traduzido = translator.translate(texto, dest=destino).text

    return jsonify({'texto_traduzido': texto_traduzido})

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
    db.create_all()
    app.run()