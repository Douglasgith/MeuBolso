from sqlalchemy.orm import Session
from src.infra.sqlalchemy.models.models import RendimentoMensal
from src.schemas.schemas import RendimentoMensalShema




class RepositorioRendimentoMensal:
    def __init__(self, db: Session):
        self.db = db

    def salvar_rendimento(self, rendimento: RendimentoMensalShema) -> RendimentoMensal:
        novo_rendimento = RendimentoMensal(
            mes=rendimento.mes,
            valor=rendimento.valor     
        )
        self.db.add(novo_rendimento)
        self.db.commit()
        self.db.refresh(novo_rendimento)
        return novo_rendimento

    def listar_rendimentos(self) -> list[RendimentoMensal]:
        rendimentos = self.db.query(RendimentoMensal).all()
        return rendimentos
        