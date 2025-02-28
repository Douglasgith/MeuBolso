from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.schemas.schemas import UsuarioSchema, UsuarioResponseSchema
from src.infra.sqlalchemy.repositorios.usuario_repositorio import RepositorioUsuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"], dependencies=[])

@router.post("/", response_model=UsuarioResponseSchema)
def cadastrar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    repo = RepositorioUsuario(db)

    if repo.buscar_por_email(usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    return repo.criar_usuario(usuario)

@router.get("/", response_model=list[UsuarioResponseSchema])
def listar_usuarios(db: Session = Depends(get_db)):
    repo = RepositorioUsuario(db)
    return repo.listar_todos()
