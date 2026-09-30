Projeto - Aplicação para acompanhamento de tarefas.

Aplicação que tem como base um CRUD, para manipulação das informações e comunicação com o banco de dados.

-Linguagem: Python.
-Bibliotecas: FastAPI, Pydantic, SQLAlchemy e SQlite.
-Plataforma Docker utilizada para containerização da aplicação.

Como clonar o repositório:
-No terminal: git clone https://github.com/MaziaB/App_Tarefas_EBAC.git
-Entre na pasta cd App_Tarefas_EBAC
-Confira se existe um Dockerfile: dir. Você vai encontrar algo como: 
Dockerfile
requirements.txt
app.py

Para construir a imagem:
-Comando no terminal: 'podman build -t app.py .'.
-Comando para rodar a imagem: 'podman run --env-file .env -d -p 8000:8000 app.py'