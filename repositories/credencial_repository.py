from database.connection import SessionLocal

from models.entities import Credencial


class CredencialRepository:

    def listar(self):

        with SessionLocal() as session:

            return (
                session.query(Credencial)
                .order_by(
                    Credencial.sistema,
                    Credencial.id,
                )
                .all()
            )

    def buscar_por_id(
        self,
        credencial_id,
    ):

        with SessionLocal() as session:

            return (
                session.query(Credencial)
                .filter(
                    Credencial.id == credencial_id
                )
                .first()
            )

    def buscar_global(
        self,
        sistema,
    ):

        with SessionLocal() as session:

            return (
                session.query(Credencial)
                .filter(
                    Credencial.sistema == sistema,
                    Credencial.tipo_vinculo == "GLOBAL",
                    Credencial.ativa.is_(True),
                )
                .order_by(
                    Credencial.id.desc()
                )
                .first()
            )

    def buscar_por_estabelecimento(
        self,
        sistema,
        filial_id,
    ):

        with SessionLocal() as session:

            return (
                session.query(Credencial)
                .filter(
                    Credencial.sistema == sistema,
                    Credencial.tipo_vinculo == "ESTABELECIMENTO",
                    Credencial.filial_id == filial_id,
                    Credencial.ativa.is_(True),
                )
                .order_by(
                    Credencial.id.desc()
                )
                .first()
            )

    def criar(
        self,
        sistema,
        tipo_vinculo,
        empresa_id,
        filial_id,
        usuario,
        chave_cofre,
    ):

        with SessionLocal() as session:

            credencial = Credencial(
                sistema=sistema,
                tipo_vinculo=tipo_vinculo,
                empresa_id=empresa_id,
                filial_id=filial_id,
                usuario=usuario,
                chave_cofre=chave_cofre,
                ativa=True,
            )

            session.add(
                credencial
            )

            session.commit()

            session.refresh(
                credencial
            )

            return credencial
