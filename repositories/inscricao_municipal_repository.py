from database.connection import SessionLocal
from models.entities import InscricaoMunicipal


class InscricaoMunicipalRepository:

    def listar(self):
        with SessionLocal() as session:
            return (
                session.query(InscricaoMunicipal)
                .order_by(
                    InscricaoMunicipal.uf,
                    InscricaoMunicipal.municipio,
                    InscricaoMunicipal.numero,
                )
                .all()
            )

    def listar_por_empresa(self, empresa_id):
        with SessionLocal() as session:
            return (
                session.query(InscricaoMunicipal)
                .filter(
                    InscricaoMunicipal.empresa_id == empresa_id
                )
                .order_by(
                    InscricaoMunicipal.uf,
                    InscricaoMunicipal.municipio,
                    InscricaoMunicipal.numero,
                )
                .all()
            )

    def listar_por_estabelecimento(self, filial_id):
        with SessionLocal() as session:
            return (
                session.query(InscricaoMunicipal)
                .filter(
                    InscricaoMunicipal.filial_id == filial_id
                )
                .order_by(
                    InscricaoMunicipal.uf,
                    InscricaoMunicipal.municipio,
                    InscricaoMunicipal.numero,
                )
                .all()
            )

    def buscar_existente(
        self,
        empresa_id,
        filial_id,
        municipio,
        uf,
        numero,
    ):
        with SessionLocal() as session:
            return (
                session.query(InscricaoMunicipal)
                .filter(
                    InscricaoMunicipal.empresa_id == empresa_id,
                    InscricaoMunicipal.filial_id == filial_id,
                    InscricaoMunicipal.municipio == municipio,
                    InscricaoMunicipal.uf == uf,
                    InscricaoMunicipal.numero == numero,
                )
                .first()
            )

    def criar(
        self,
        empresa_id,
        filial_id,
        municipio,
        uf,
        numero,
        ativa,
    ):
        with SessionLocal() as session:

            inscricao = InscricaoMunicipal(
                empresa_id=empresa_id,
                filial_id=filial_id,
                municipio=municipio,
                uf=uf,
                numero=numero,
                ativa=ativa,
            )

            session.add(inscricao)
            session.commit()
            session.refresh(inscricao)

            return inscricao
