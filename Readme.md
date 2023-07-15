# API de registro de atividades

Esta é uma API de exemplo que permite cadastrar, listar e deletar atividades em um banco de dados PostgreSQL. A API é implementada em Flask e utiliza o Flask-CORS para permitir a comunicação com outros domínios. Além disso, possui documentação do Swagger/OpenAPI para facilitar o entendimento e uso da API.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados em sua máquina:

- Python 3.x
- PostgreSQL (com um banco de dados configurado)

## Instalação

## Crie e ative um ambiente virtual (recomendado):
python -m venv env  # cria o ambiente virtual
source env/bin/activate  # ativa o ambiente virtual (Linux/Mac)
env\Scripts\activate  # ativa o ambiente virtual (Windows)

## Instale as dependências do projeto:
```
pip install -r requirements.txt
```

## Configuração do Banco de Dados:
- Certifique-se de ter um servidor PostgreSQL em execução e um banco de dados configurado.
- Abra o arquivo scriptSQL.py dentro da da pasta DB, altere nas linhas 7 e 26 o password para a senha que foi criada ao configurar o postgre.
- No arquivo app.py, altere as informações de conexão do banco de dados no método cursor_DB() de acordo com suas configurações

## Execute o aplicativo Flask:
python app.py

## Documentação
Acesse a documentação do Swagger:

Abra seu navegador e visite: http://localhost:5000/swagger

A documentação do Swagger fornecerá informações detalhadas sobre as rotas, parâmetros e respostas da API.

