from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.schemas import schemas
from src.infra.sqlalchemy.repositorios.rendimento_mensal import RepositorioRendimentoMensal
from src.infra.routers.auth import verificador_token

router = APIRouter(prefix="/rendimento", tags=["Rendimentos"])

# Rota para criar um rendimento mensal
@router.post("/", response_model=schemas.RendimentoMensalShema)
def criar_rendimento(
    rendimento: schemas.RendimentoMensalShema,
    db: Session = Depends(get_db),
    usuario=Depends(verificador_token)
):
    repositorio = RepositorioRendimentoMensal(db)
    rendimento.usuario_id = usuario.id
    return repositorio.salvar_rendimento(rendimento)

# Rota para listar todos os rendimentos mensais
@router.get("/", response_model=list[schemas.RendimentoMensalShema])
def listar_rendimentos(db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioRendimentoMensal(db)
    return repositorio.listar_rendimentos()
