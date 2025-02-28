import re
from datetime import date 
from pydantic import BaseModel, EmailStr, validator
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
    usuario_id: Optional[int] = None 

    class Config:
        from_attributes = True 

 
class RendimentoMensalShema(BaseModel):
    id: Optional[int] = None
    mes: str
    valor : float
    usuario_id: Optional[int] = None 
    
    class Config:
        from_attributes = True

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

    @validator('nome')
    def validar_nome(cls, value):
        if not re.match('^([a-z]|[0-9]|@)+$', value):
            raise ValueError("Formato do nome invalido")
        return value

class UsuarioResponseSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True
