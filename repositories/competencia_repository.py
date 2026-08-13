from database.connection import SessionLocal
from models.entities import Competencia


class CompetenciaRepository:

    def listar(self):
        with SessionLocal() as session:
            return (
                session.query(Competencia)
                .order_by(
                    Competencia.ano.desc(),
                    Competencia.mes.desc(),
                )
                .all()
            )

    def listar_por_empresa(self, empresa_id):
        with SessionLocal() as session:
            return (
                session.query(Competencia)
                .filter(
                    Competencia.empresa_id == empresa_id
                )
                .order_by(
                    Competencia.ano.desc(),
                    Competencia.mes.desc(),
                )
                .all()
            )

    def listar_por_estabelecimento(
        self,
        empresa_id,
        filial_id,
    ):
        with SessionLocal() as session:
            return (
                session.query(Competencia)
                .filter(
                    Competencia.empresa_id == empresa_id,
                    Competencia.filial_id == filial_id,
                )
                .order_by(
                    Competencia.ano.desc(),
                    Competencia.mes.desc(),
                )
                .all()
            )

    def buscar_existente(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
    ):
        with SessionLocal() as session:
            return (
                session.query(Competencia)
                .filter(
                    Competencia.empresa_id == empresa_id,
                    Competencia.filial_id == filial_id,
                    Competencia.mes == mes,
                    Competencia.ano == ano,
                )
                .first()
            )

    def criar(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
        data_entrega,
        data_vencimento,
        status,
    ):
        with SessionLocal() as session:

            competencia = Competencia(
                empresa_id=empresa_id,
                filial_id=filial_id,
                mes=mes,
                ano=ano,
                data_entrega=data_entrega,
                data_vencimento=data_vencimento,
                status=status,
            )

            session.add(
                competencia
            )

            session.commit()

            session.refresh(
                competencia
            )

            return competencia
