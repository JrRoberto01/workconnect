# Usa uma imagem base do Python
FROM python:latest

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY . /app

# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# Comando padrão para iniciar o servidor Django
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "workconnect.asgi:application"]