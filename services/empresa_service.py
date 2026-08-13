from pathlib import Path

from repositories.empresa_repository import EmpresaRepository


class EmpresaService:
    def __init__(self):
        self.repository = EmpresaRepository()

    def listar(self):
        return self.repository.listar()

    def criar(
        self,
        razao_social,
        nome_fantasia,
        cnpj,
        diretorio_base,
    ):
        razao_social = razao_social.strip()
        nome_fantasia = nome_fantasia.strip()
        cnpj = self.normalizar_cnpj(cnpj)
        diretorio_base = diretorio_base.strip()

        if not razao_social:
            raise ValueError("Razão social é obrigatória.")

        if not cnpj:
            raise ValueError("CNPJ é obrigatório.")

        if len(cnpj) != 14:
            raise ValueError("O CNPJ deve possuir 14 números.")

        empresa_existente = self.repository.buscar_por_cnpj(cnpj)

        if empresa_existente:
            raise ValueError(
                "Já existe uma empresa cadastrada com este CNPJ."
            )

        if not diretorio_base:
            raise ValueError("Diretório base é obrigatório.")

        caminho = Path(diretorio_base)

        if not caminho.exists():
            raise ValueError(
                "O diretório informado não existe ou não está acessível."
            )

        if not caminho.is_dir():
            raise ValueError(
                "O caminho informado não é um diretório."
            )

        return self.repository.criar(
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            cnpj=cnpj,
            diretorio_base=str(caminho),
        )

    def normalizar_cnpj(self, cnpj):
        return "".join(
            caractere
            for caractere in cnpj
            if caractere.isdigit()
        )
