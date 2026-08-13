from repositories.filial_repository import (
    FilialRepository,
)


UFS_BRASIL = {
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
}


TIPOS_ESTABELECIMENTO = {
    "MATRIZ",
    "FILIAL",
}


class FilialService:

    def __init__(self):
        self.repository = (
            FilialRepository()
        )

    def listar(self):
        return (
            self.repository.listar()
        )

    def listar_por_empresa(
        self,
        empresa_id,
    ):
        return (
            self.repository
            .listar_por_empresa(
                empresa_id
            )
        )

    def criar(
        self,
        empresa_id,
        identificacao,
        cnpj,
        uf,
        municipio,
        tipo,
    ):
        identificacao = (
            identificacao
            .strip()
        )

        cnpj = (
            self.normalizar_cnpj(
                cnpj
            )
        )

        uf = (
            uf
            .strip()
            .upper()
        )

        municipio = (
            municipio
            .strip()
        )

        tipo = (
            tipo
            .strip()
            .upper()
        )

        if not empresa_id:

            raise ValueError(
                "Selecione uma empresa."
            )

        if not identificacao:

            raise ValueError(
                "A identificação do estabelecimento "
                "é obrigatória."
            )

        if not cnpj:

            raise ValueError(
                "O CNPJ do estabelecimento "
                "é obrigatório."
            )

        if len(cnpj) != 14:

            raise ValueError(
                "O CNPJ deve possuir "
                "14 números."
            )

        if uf not in UFS_BRASIL:

            raise ValueError(
                "Informe uma UF válida."
            )

        if tipo not in TIPOS_ESTABELECIMENTO:

            raise ValueError(
                "Selecione MATRIZ ou FILIAL."
            )

        existente = (
            self.repository
            .buscar_por_cnpj(
                cnpj
            )
        )

        if existente:

            raise ValueError(
                "Já existe um estabelecimento "
                "cadastrado com este CNPJ."
            )

        return (
            self.repository.criar(
                empresa_id=empresa_id,
                identificacao=identificacao,
                cnpj=cnpj,
                uf=uf,
                municipio=municipio or None,
                tipo=tipo,
            )
        )

    def normalizar_cnpj(
        self,
        cnpj,
    ):
        return "".join(
            caractere
            for caractere in cnpj
            if caractere.isdigit()
        )
