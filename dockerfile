# Use a imagem base do Python
FROM python:3.11.4

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os requisitos do projeto para o contêiner
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta em que a aplicação Flask está rodando (por padrão, a porta 5000)
EXPOSE 5000

# Inicialize a aplicação Flask quando o contêiner for iniciado
CMD ["python", "app.py"]
