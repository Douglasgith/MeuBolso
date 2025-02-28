
from fastapi import status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import Session
from src.schemas.schemas import UsuarioSchema
from src.infra.sqlalchemy.models.models import Usuario


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RepositorioUsuario:
    def __init__(self, db: Session):
        self.db = db

    def criar_usuario(self, usuario: UsuarioSchema) -> Usuario:
        senha_hash = pwd_context.hash(usuario.senha)
        novo_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash=senha_hash
        )
        try:
            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado"
            )
        return novo_usuario
    
    def buscar_por_email(self, email:str) -> Usuario:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def listar_todos(self)->list[Usuario]:
        usuarios = self.db.query(Usuario).all()
        return usuarios


    def verificar_nome(self, nome: str) -> Usuario:
        return self.db.query(Usuario).filter(Usuario.nome == nome).first()

    def verificar_senha(self, senha_plana: str, senha_hash: str) -> bool:
        return pwd_context.verify(senha_plana, senha_hash)

