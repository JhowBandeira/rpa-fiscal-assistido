from database.connection import SessionLocal
from models.entities import InscricaoEstadual


class InscricaoEstadualRepository:

    def listar(self):
        with SessionLocal() as session:
            return (
                session.query(InscricaoEstadual)
                .order_by(
                    InscricaoEstadual.uf,
                    InscricaoEstadual.numero,
                )
                .all()
            )

    def listar_por_empresa(self, empresa_id):
        with SessionLocal() as session:
            return (
                session.query(InscricaoEstadual)
                .filter(
                    InscricaoEstadual.empresa_id == empresa_id
                )
                .order_by(
                    InscricaoEstadual.uf,
                    InscricaoEstadual.numero,
                )
                .all()
            )

    def listar_por_estabelecimento(self, filial_id):
        with SessionLocal() as session:
            return (
                session.query(InscricaoEstadual)
                .filter(
                    InscricaoEstadual.filial_id == filial_id
                )
                .order_by(
                    InscricaoEstadual.uf,
                    InscricaoEstadual.numero,
                )
                .all()
            )

    def buscar_existente(
        self,
        empresa_id,
        filial_id,
        uf,
        numero,
    ):
        with SessionLocal() as session:
            return (
                session.query(InscricaoEstadual)
                .filter(
                    InscricaoEstadual.empresa_id == empresa_id,
                    InscricaoEstadual.filial_id == filial_id,
                    InscricaoEstadual.uf == uf,
                    InscricaoEstadual.numero == numero,
                )
                .first()
            )

    def criar(
        self,
        empresa_id,
        filial_id,
        uf,
        numero,
        emitir_cnd,
        ativa,
    ):
        with SessionLocal() as session:

            inscricao = InscricaoEstadual(
                empresa_id=empresa_id,
                filial_id=filial_id,
                uf=uf,
                numero=numero,
                emitir_cnd=emitir_cnd,
                ativa=ativa,
            )

            session.add(inscricao)
            session.commit()
            session.refresh(inscricao)

            return inscricao
