from repositories.inscricao_estadual_repository import (
    InscricaoEstadualRepository,
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


class InscricaoEstadualService:

    def __init__(self):
        self.repository = InscricaoEstadualRepository()

    def listar(self):
        return self.repository.listar()

    def listar_por_empresa(self, empresa_id):
        return self.repository.listar_por_empresa(
            empresa_id
        )

    def listar_por_estabelecimento(self, filial_id):
        return self.repository.listar_por_estabelecimento(
            filial_id
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

        if uf not in UFS_BRASIL:
            raise ValueError(
                "Informe uma UF válida."
            )

        if not numero:
            raise ValueError(
                "A Inscrição Estadual é obrigatória."
            )

        existente = self.repository.buscar_existente(
            empresa_id=empresa_id,
            filial_id=filial_id,
            uf=uf,
            numero=numero,
        )

        if existente:
            raise ValueError(
                "Esta Inscrição Estadual já está cadastrada "
                "para este estabelecimento."
            )

        return self.repository.criar(
            empresa_id=empresa_id,
            filial_id=filial_id,
            uf=uf,
            numero=numero,
            emitir_cnd=emitir_cnd,
            ativa=ativa,
        )
