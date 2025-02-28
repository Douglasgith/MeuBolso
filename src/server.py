from fastapi import FastAPI, Depends, HTTPException, status
from src.infra.routers import auth, usuarios, controle_mensal, rendimento
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.infra.sqlalchemy.config.database import get_db, create_db_and_tables
from src.infra.sqlalchemy.models.models import ControleMensal, Categoria, FormaDePagamento, Mes
from src.infra.sqlalchemy.repositorios.controle_mensal import RepositorioControleMensal
from src.infra.sqlalchemy.repositorios.rendimento_mensal import RepositorioRendimentoMensal
from src.infra.sqlalchemy.repositorios.usuario_repositorio import RepositorioUsuario
from src.schemas import schemas
from src.schemas.schemas import UsuarioSchema, UsuarioResponseSchema
from src.infra.sqlalchemy.models.models import Usuario
from sqlalchemy.orm import Session
from src.utils.exceptions import AppException




app = FastAPI()
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(controle_mensal.router)
app.include_router(rendimento.router)

@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Endpoints CRUD
'''
# Rota para criar um controle mensal
@app.post("/controle-mensal/", response_model=schemas.ControleMensalSchema)
def criar_controle_mensal(controle_mensal: schemas.ControleMensalSchema, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.criar(controle_mensal)

# Rota para listar todos os controles mensais
@app.get("/controle-mensal/", response_model=list[schemas.ControleMensalSchema])
def listar_controle_mensal(db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.listar()

#Rota para buscar um controle mensal pelo id
@app.get("/controle-mensal/{controle_mensal_id}", response_model=schemas.ControleMensalSchema)
def buscar_controle_mensal(controle_mensal_id: int, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_id(controle_mensal_id)

# Rota para atualizar um controle mensal
@app.put("/controle-mensal/{controle_mensal_id}", response_model=schemas.ControleMensalSchema)
def update_controle_mensal(controle_mensal_id: int, controle_mensal: schemas.ControleMensalSchema, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.atualizar(controle_mensal_id, controle_mensal)

#Rota para deletar um controle mensal
@app.delete("/controle-mensal/{controle_mensal_id}")
def delete_controle_mensal(controle_mensal_id: int, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.deletar(controle_mensal_id)

#Rota para buscar um controle mensal pelo mês
@app.get("/controle-mensal/mes/{mes}", response_model=list[schemas.ControleMensalSchema])
def buscar_controle_mensal_por_mes(mes: Mes, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_mes(mes)

#Rota para buscar um controle mensal pela categoria
@app.get("/controle-mensal/categoria/{categoria}", response_model=list[schemas.ControleMensalSchema])
def buscar_controle_mensal_por_categoria(categoria: Categoria, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_categoria(categoria)

#Rota para buscar um controle mensal pela forma de pagamento
@app.get("/controle-mensal/forma-de-pagamento/{forma_de_pagamento}", response_model=list[schemas.ControleMensalSchema])
def buscar_controle_mensal_por_forma_de_pagamento(forma_de_pagamento: FormaDePagamento, db: Session = Depends(get_db)):
    repositorio = RepositorioControleMensal(db)
    return repositorio.buscar_por_forma_de_pagamento(forma_de_pagamento)

#Rota rendimento

# Rota para criar um rendimento mensal
@app.post("/rendimento/", response_model=schemas.RendimentoMensalShema)
def criar_rendimento(rendimento: schemas.RendimentoMensalShema, db: Session = Depends(get_db)):
    repositorio = RepositorioRendimentoMensal(db)
    return repositorio.salvar_rendimento(rendimento)

# Rota para listar todos os rendimentos mensais
@app.get("/rendimentos/", response_model=list[schemas.RendimentoMensalShema])
def listar_rendimentos(db: Session = Depends(get_db)):
    repositorio = RepositorioRendimentoMensal(db)
    return repositorio.listar_rendimentos()

'''