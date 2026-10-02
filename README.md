Projeto - Aplicação para acompanhamento de tarefas.

Aplicação que tem como base um CRUD, para manipulação das informações e comunicação com o banco de dados.

-Linguagem: Python.
-Bibliotecas: FastAPI, Pydantic, SQLAlchemy e SQlite.
-Plataforma Docker utilizada para containerização da aplicação.

Como clonar o repositório:
-No terminal: git clone https://github.com/MaziaB/App_Tarefas_EBAC.git
-Entre na pasta cd App_Tarefas_EBAC
-Confira se existe um Dockerfile: dir. 
Você vai encontrar algo como: 
Dockerfile
app.py

Comandos no terminal para construir e executar a imagem:
-'podman machine init'
-'podman machine start'
-'podman-compose build'
-'podman-compose up -d'
