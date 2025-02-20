from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models.models import ControleMensal
from src.schemas import schemas
from fastapi import HTTPException
from src.utils.exceptions import RegistroNaoEncontradoException, ErroNoBancoDeDadosException, ErroNaBuscaPorMesException



class RepositorioControleMensal(): 
    # Repositório para operações relacionadas ao controle mensal
    def __init__(self, db: Session):
        self.db = db
    def criar(self, controle_mensal: schemas.ControleMensalSchema) -> schemas.ControleMensalSchema:  
            #Cria um novo registro de controle mensal no banco de dados.
        #Args:
            #controle_mensal (schemas.ControleMensalSchema): Dados do controle mensal a serem criados
        #Returns:
            #schemas.ControleMensalSchema: O registro criado, serializado no schema Pydantic.
            # Converte o schema Pydantic para um objeto SQLAlchemy
            db_controle_mensal = ControleMensal(
                mes=controle_mensal.mes,
                data=controle_mensal.data,
                estabelecimento=controle_mensal.estabelecimento,
                categoria=controle_mensal.categoria,
                forma_de_pagamento=controle_mensal.forma_de_pagamento,
                numero_de_parcelas=controle_mensal.numero_de_parcelas,
                qntd_parcelas_pagas=controle_mensal.qntd_parcelas_pagas,
                valor_da_parcela=controle_mensal.valor_da_parcela
            )
            # Adiciona e persiste o objeto no banco de dados
            self.db.add(db_controle_mensal)
            self.db.commit()
            self.db.refresh(db_controle_mensal)
            # Converte o objeto SQLAlchemy de volta para o schema Pydantic
            return schemas.ControleMensalSchema.from_orm(db_controle_mensal)

    def listar(self) -> list[schemas.ControleMensalSchema]:
        #Lista todos os registros de controle mensal no banco de dados.
        # #Returns:
        #list[schemas.ControleMensalSchema]: Lista de registros serializados no schema Pydantic.
        # Busca todos os registros no banco de dados
        controle_mensal = self.db.query(ControleMensal).all()
        # Converte a lista de objetos SQLAlchemy para uma lista de schemas Pydantic
        return [schemas.ControleMensalSchema.from_orm(db_controle_mensal) for db_controle_mensal in controle_mensal]

    def buscar_por_id(self, controle_mensal_id: int) -> schemas.ControleMensalSchema:
        db_controle_mensal = self.db.query(ControleMensal).filter(ControleMensal.id == controle_mensal_id).first()
        if db_controle_mensal is None:
            raise RegistroNaoEncontradoException()
        return db_controle_mensal


    def atualizar(self, controle_mensal_id: int, controle_mensal: schemas.ControleMensalSchema) -> schemas.ControleMensalSchema:
        db_controle_mensal = self.db.query(ControleMensal).filter(ControleMensal.id == controle_mensal_id).first()
        if db_controle_mensal is None:
            raise RegistroNaoEncontradoException()
        
        for key, value in controle_mensal.dict().items():
            setattr(db_controle_mensal, key, value)

        self.db.commit()
        self.db.refresh(db_controle_mensal)
        return db_controle_mensal
    
    def deletar(self, controle_mensal_id: int):
        delete_control = self.db.query(ControleMensal).filter(ControleMensal.id == controle_mensal_id).first()
        if delete_control is None:
            raise RegistroNaoEncontradoException()
        self.db.delete(delete_control)
        self.db.commit()
        return {"detail": "Registro deletado com sucesso"}

    def buscar_por_mes(self, mes: str) -> list[schemas.ControleMensalSchema]:
        db_controle_mensal = self.db.query(ControleMensal).filter(ControleMensal.mes == mes).all()
        print (db_controle_mensal)
        if db_controle_mensal is None or len(db_controle_mensal) == 0:
            raise ErroNaBuscaPorMesException()
        return db_controle_mensal
    
    def buscar_por_categoria(self, categoria: str) -> list[schemas.ControleMensalSchema]:
        db_controle_mensal = self.db.query(ControleMensal).filter(ControleMensal.categoria == categoria).all()
        if db_controle_mensal is None or len(db_controle_mensal) == 0:
            raise RegistroNaoEncontradoException()
        return db_controle_mensal
    
    def buscar_por_forma_de_pagamento(self, forma_de_pagamento: str) -> list[schemas.ControleMensalSchema]:
        db_controle_mensal = self.db.query(ControleMensal).filter(ControleMensal.forma_de_pagamento == forma_de_pagamento).all()
        if db_controle_mensal is None or len(db_controle_mensal) == 0:
            raise RegistroNaoEncontradoException()
        return db_controle_mensal
    
