import re
from datetime import date 
from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Optional


from src.infra.sqlalchemy.models.models import Categoria, FormaDePagamento, Mes

class ControleMensalSchema(BaseModel):
    id: Optional[int] = None
    data : date = date.today()
    mes: str = date.today().strftime('%m')
    estabelecimento: str 
    categoria: str
    forma_de_pagamento: str
    parcelado: bool

    numero_de_parcelas: Optional[int] = 1 
    qntd_parcelas_pagas: Optional[int] = 0 
    valor_da_parcela: Optional[float] = None
    valor_total: float
    usuario_id: Optional[int] = None 

    # Valida a data e preenche com a data atual caso não seja informada:( e ideia que não seja informada)
    @field_validator('data', mode='before')
    @classmethod
    def preencher_data(cls,value):
        if value is None:
            value = date.today()

        return value
    
    # valida o mes e preenche o mes baseado na data caso não seja informado
    @field_validator('mes', mode='before')
    @classmethod
    def preencher_mes(cls,value, values):
        if value is None:
            data = values.get('data') or date.today()  # Usa a data fornecida ou a data atual
            mes = data.strftime('%m')  # Formato MM (01 a 12)
            return mes
        return value
    
    
    # Calcula o valor da parcela baseado no valor total e no numero de parcelas
    @field_validator('valor_da_parcela', mode='before')
    @classmethod
    def calcular_valor_parcela(cls,value, info):
        if info.data.get('parcelado', False):
            valor_total = info.data.get('valor_total', 0.0)
            numero_de_parcelas = info.data.get('numero_de_parcelas', 1)
            if valor_total > 0 and numero_de_parcelas > 0:
                return valor_total / numero_de_parcelas
        return info.data.get('valor_total', 0.0)

    # Se a compra não for parcelada, o numero de parcelas é 1 e a quantidade de parcelas pagas é 0
    @field_validator('numero_de_parcelas','qntd_parcelas_pagas', mode='before')
    @classmethod
    def ajustar_parcelas(cls, value, info):
        if info.data.get('parcelado') is False:
            return 1 if info.field_name == 'numero_de_parcelas' else 0
        return value
    
    #Valida se o valor_total foi fornecido e é positivo.
    @field_validator('valor_total', mode='before')
    @classmethod
    def validar_valor_total(cls, value):
        if value is None:
            raise ValueError("O campo 'valor_total' não pode ser None.")
        if value <= 0:
            raise ValueError("O campo 'valor_total' deve ser maior que zero.")
        return value


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
