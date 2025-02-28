from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.schemas import schemas
from src.infra.sqlalchemy.repositorios.controle_mensal import RepositorioControleMensal
from src.infra.sqlalchemy.models.models import ControleMensal, Categoria, FormaDePagamento, Mes
from src.infra.routers.auth import verificador_token

router = APIRouter(prefix="/controle-mensal", tags=["Controle Mensal"])

# Rota para criar um controle mensal
@router.post("/", response_model=schemas.ControleMensalSchema)
def criar_controle_mensal(
    controle_mensal: schemas.ControleMensalSchema,
    db: Session = Depends(get_db),
    usuario=Depends(verificador_token)
):
    repositorio = RepositorioControleMensal(db)
    controle_mensal.usuario_id = usuario.id
    return repositorio.criar(controle_mensal)

# Rota para listar todos os controles mensais
@router.get("/", response_model=list[schemas.ControleMensalSchema])
def listar_controle_mensal(db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio

#Rota para buscar um controle mensal pelo id
@router.get("/{controle_mensal_id}", response_model=schemas.ControleMensalSchema)
def buscar_controle_mensal(controle_mensal_id: int, db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_id(controle_mensal_id)

# Rota para atualizar um controle mensal
@router.put("/{controle_mensal_id}", response_model=schemas.ControleMensalSchema)
def atualizar_controle_mensal(controle_mensal_id: int, db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.atualizar(controle_mensal_id)

#Rota para deletar um controle mensal
@router.delete("/controle-mensal/{controle_mensal_id}", response_model=schemas.ControleMensalSchema)
def delete_controle_mensal(controle_mensal_id: int, db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.deletar(controle_mensal_id)

#Rota para buscar um controle mensal pelo mês
@router.get("/controle-mensal/mes/{mes}", response_model=list[schemas.ControleMensalSchema])
def buscar_controle_mensal_por_mes(mes: Mes, db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_mes(mes)

#Rota para buscar um controle mensal pela categoria
@router.get("/controle-mensal/categoria/{categoria}", response_model=list[schemas.ControleMensalSchema])
def buscar_controle_mensal_por_categoria(categoria: Categoria, db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_categoria(categoria)

#Rota para buscar um controle mensal pela forma de pagamento
@router.get("/controle-mensal/forma-de-pagamento/{forma_de_pagamento}", response_model=list[schemas.ControleMensalSchema])
def buscar_controle_mensal_por_forma_de_pagamento(forma_de_pagamento: FormaDePagamento, db: Session = Depends(get_db), usuario=Depends(verificador_token)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_forma_de_pagamento(forma_de_pagamento)