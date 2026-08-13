from database.connection import SessionLocal
from models.entities import Empresa


class EmpresaRepository:

    def listar(self):
        with SessionLocal() as session:
            return (
                session.query(Empresa)
                .order_by(Empresa.razao_social)
                .all()
            )

    def buscar_por_id(self, empresa_id):
        with SessionLocal() as session:
            return (
                session.query(Empresa)
                .filter(Empresa.id == empresa_id)
                .first()
            )

    def buscar_por_cnpj(self, cnpj):
        with SessionLocal() as session:
            return (
                session.query(Empresa)
                .filter(Empresa.cnpj == cnpj)
                .first()
            )

    def criar(
        self,
        razao_social,
        nome_fantasia,
        cnpj,
        diretorio_base,
    ):
        with SessionLocal() as session:
            empresa = Empresa(
                razao_social=razao_social,
                nome_fantasia=nome_fantasia,
                cnpj=cnpj,
                diretorio_base=diretorio_base,
            )

            session.add(empresa)
            session.commit()
            session.refresh(empresa)

            return empresa
