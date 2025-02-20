from datetime import date 
from pydantic import BaseModel, EmailStr
from typing import Optional


from src.infra.sqlalchemy.models.models import Categoria, FormaDePagamento, Mes

class ControleMensalSchema(BaseModel):
    id: Optional[int] = None
    mes: Mes
    data : date
    estabelecimento: str 
    categoria: Categoria
    forma_de_pagamento: FormaDePagamento
    numero_de_parcelas: int 
    qntd_parcelas_pagas: int 
    valor_da_parcela: float

    class Config:
        from_attributes = True 

 
class RendimentoMensalShema(BaseModel):
    id: Optional[int] = None
    mes: str
    valor : float
    
    class Config:
        from_attributes = True

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioResponseSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True
