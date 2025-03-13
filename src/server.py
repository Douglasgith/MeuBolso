from fastapi import FastAPI
from src.infra.routers import auth, usuarios, controle_mensal, rendimento
from fastapi.responses import JSONResponse
from src.infra.sqlalchemy.config.database import create_db_and_tables
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
