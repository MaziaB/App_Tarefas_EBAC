from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os
import subprocess

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")

security = HTTPBasic()

class TarefaDB(Base):
    __tablename__="Tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome_tarefa = Column(String, index=True)
    descricao_tarefa = Column(String, index=True)
    concluida = Column(Boolean, default=False, nullable=False)

class Tarefa(BaseModel):
    nome_tarefa: str
    descricao_tarefa: str
    concluida: bool = False

Base.metadata.create_all(bind=engine)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos!",
            headers={"WWW-Authenticate": "Basic"}
        )

@app.post("/nova-tarefa")
def post_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome_tarefa == tarefa.nome_tarefa, TarefaDB.descricao_tarefa == tarefa.descricao_tarefa).first()
    if db_tarefa:
       raise HTTPException(status_code=400, detail="Tarefa já cadastrada!")
    
    tarefa_atualizada = TarefaDB(nome_tarefa=tarefa.nome_tarefa, descricao_tarefa=tarefa.descricao_tarefa, concluida=tarefa.concluida)
    db.add(tarefa_atualizada)
    db.commit()
    db.refresh(tarefa_atualizada)
    
    return {"message": "Nova tarefa cadastrada com sucesso!"}


@app.get("/tarefas")
def get_tarefas(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos!")

    tarefas = db.query(TarefaDB).offset((page - 1)*limit).limit(limit).all()
    
    if not tarefas:
        return {"message": "Nenhuma tarefa cadastrada!"}

    return {
           "page": page,
           "size": limit,
           "lista": tarefas,
           "tarefas": [{"nome_tarefa": tdata.nome_tarefa, "descricao_tarefa": tdata.descricao_tarefa, "concluida": tdata.concluida}
                   for tdata in tarefas]
        }


@app.put("/status-da-tarefa")
def put_tarefas(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome_tarefa == tarefa.nome_tarefa).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não cadastrada!")
    
    db_tarefa.nome_tarefa = tarefa.nome_tarefa
    db_tarefa.descricao_tarefa = tarefa.descricao_tarefa
    db_tarefa.concluida = tarefa.concluida
    db.commit()
    db.refresh(db_tarefa)
    
    return {"Message": "Status da tarefa atualizado com sucesso!"}


@app.delete("/excluir-tarefa")
def delete_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.nome_tarefa == tarefa.nome_tarefa).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não cadastrada!")
    
    db.delete(db_tarefa)
    db.commit()
    
    return {"message": "Tarefa excluída com sucesso!"}
