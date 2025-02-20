from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
import os
from src.utils.exceptions import ErroNoBancoDeDadosException


class Base(SQLModel):
    """
    Classe base para todos os modelos do SQLAlchemy.
    """
    pass

# Criar caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório atual
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'gastos.db')}"  # Caminho absoluto

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)  # echo=True para debug

# Criar a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """
    Cria todas as tabelas no banco de dados com base nos modelos SQLModel.
    """
    SQLModel.metadata.create_all(engine)

def get_db():
    """
    Retorna uma instância da sessão do banco de dados.
    """ 
    db = SessionLocal()
    try:
        yield db
        db.commit()  # Garante que as mudanças sejam salvas
    except Exception as e:
        db.rollback()  # Reverte em caso de erro
        raise e
    finally:
        db.close()
