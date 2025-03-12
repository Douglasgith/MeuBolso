from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, List
from datetime import date


# Enums
class Categoria(str, Enum):
    aluguel = "aluguel"
    energia = "energia"
    agua = "agua"
    condominio = "condominio"
    internet = "internet"
    supermercado = "supermercado"
    farmacia = "farmacia"
    transporte = "transporte"
    plano_de_cell = "plano de cell"
    gas = "gas"
    despesas_carro = "despesas carro"
    Pet = "Pet"
    manutencao_casa = "manutenção casa"
    lazer = "lazer"
    educacao = "educacao"
    plano_de_saude = "plano de saude"
    plano_de_odonto = "plano de odonto"
    academia = "academia"
    assinaturas_mensais = "assinaturas mensais"
    cuidados_pessoais = "cuidados pessoais"
    torrar = "torrar"
    outros = "outros"

class FormaDePagamento(str, Enum):
    debito = "debito"
    credito = "credito"
    dinheiro = "dinheiro"
    transferencia = "transferencia"
    boleto = "boleto"
    pix = "pix"

class Mes(str, Enum):
    janeiro = "janeiro"
    fevereiro = "fevereiro"
    marco = "março"
    abril = "abril"
    maio = "maio"
    junho = "junho"
    julho = "julho"
    agosto = "agosto"
    setembro = "setembro"
    outubro = "outubro"
    novembro = "novembro"
    dezembro = "dezembro"


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=255, nullable=False, unique=True)
    email: str = Field(max_length=255, nullable=False, unique=True)
    senha_hash: str = Field(max_length=255, nullable=False)
    # Relação do usuario com controle mensal
    controles_mensais: List["ControleMensal"] = Relationship(back_populates='usuario')
    # Relação do usuario com rendimento mensal
    rendimentos_mensais: List["RendimentoMensal"] = Relationship(back_populates='usuario')


class ControleMensal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date = Field(nullable=False)
    mes: Optional[str] = Field(nullable=False)
    estabelecimento: str = Field(max_length=255, nullable=False)
    categoria: Categoria = Field(sa_column_kwargs={"nullable": False})
    forma_de_pagamento: FormaDePagamento = Field(sa_column_kwargs={"nullable": False})
    parcelado: bool = Field(default=False, nullable=False)

    numero_de_parcelas: Optional[int] = Field(default=1, nullable=False)
    qntd_parcelas_pagas: Optional[int] = Field(default=0, nullable=False)
    valor_da_parcela: Optional[float] = Field(default=0.0, nullable=False)
    valor_total: Optional[float] = Field(nullable=False)
    #Relação com usuário
    usuario_id :int = Field(foreign_key="usuario.id", nullable=False)
    usuario: Usuario = Relationship(back_populates="controles_mensais")

class RendimentoMensal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mes: str = Field(sa_column_kwargs={"nullable": False})
    valor: float = Field(nullable=False)
    #Relação com usuario
    usuario_id : int = Field(foreign_key="usuario.id", nullable=False)
    usuario: Optional[Usuario] = Relationship(back_populates="rendimentos_mensais")
