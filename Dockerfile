# usa imagem oficial do Python 3.11
FROM python:3.11-slim

# define diretório de trabalho dentro do container
WORKDIR /app

# copia requirements primeiro (melhor para cache do Docker)
COPY requirements.txt .

# instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# copia todo o projeto para dentro do container
COPY . .

# xpõe a porta usada pela API
EXPOSE 8000

# comando para iniciar FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]