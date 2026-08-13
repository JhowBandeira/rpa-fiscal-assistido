from repositories.inscricao_municipal_repository import (
    InscricaoMunicipalRepository,
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


class InscricaoMunicipalService:

    def __init__(self):
        self.repository = (
            InscricaoMunicipalRepository()
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
            self.repository.listar_por_empresa(
                empresa_id
            )
        )

    def listar_por_estabelecimento(
        self,
        filial_id,
    ):
        return (
            self.repository.listar_por_estabelecimento(
                filial_id
            )
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
        municipio = municipio.strip()
        uf = uf.strip().upper()
        numero = numero.strip()

        if not empresa_id:
            raise ValueError(
                "Selecione uma empresa."
            )

        if not filial_id:
            raise ValueError(
                "Selecione um estabelecimento."
            )

        if not municipio:
            raise ValueError(
                "O município é obrigatório."
            )

        if uf not in UFS_BRASIL:
            raise ValueError(
                "Informe uma UF válida."
            )

        if not numero:
            raise ValueError(
                "A Inscrição Municipal / CCM é obrigatória."
            )

        existente = (
            self.repository.buscar_existente(
                empresa_id=empresa_id,
                filial_id=filial_id,
                municipio=municipio,
                uf=uf,
                numero=numero,
            )
        )

        if existente:
            raise ValueError(
                "Esta Inscrição Municipal já está cadastrada "
                "para este estabelecimento."
            )

        return self.repository.criar(
            empresa_id=empresa_id,
            filial_id=filial_id,
            municipio=municipio,
            uf=uf,
            numero=numero,
            ativa=ativa,
        )
