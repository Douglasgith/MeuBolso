from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.schemas.schemas import UsuarioSchema
from src.infra.sqlalchemy.models.models import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RepositorioUsuario:
    def __init__(self, db: Session):
        self.db = db

    def criar_usuario(self, usuario: UsuarioSchema)-> Usuario:
        #has da senha antes de salar no banco
        senha_hash = pwd_context.hash(usuario.senha)
        novo_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha_hash=senha_hash)
        self.db.add(novo_usuario)
        self.db.commit()
        self.db.refresh(novo_usuario)
        return novo_usuario
    
    def buscar_por_email(self, email: str) -> Usuario:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    