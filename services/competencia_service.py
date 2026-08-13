from datetime import datetime

from repositories.competencia_repository import (
    CompetenciaRepository,
)

from repositories.empresa_repository import (
    EmpresaRepository,
)

from repositories.filial_repository import (
    FilialRepository,
)

from storage.directory_manager import (
    DirectoryManager,
)


class CompetenciaService:

    def __init__(self):

        self.repository = CompetenciaRepository()
        self.empresa_repository = EmpresaRepository()
        self.filial_repository = FilialRepository()
        self.directory_manager = DirectoryManager()

    # ============================================================
    # LISTAGENS
    # ============================================================

    def listar(self):

        return self.repository.listar()

    def listar_por_empresa(
        self,
        empresa_id,
    ):

        return self.repository.listar_por_empresa(
            empresa_id
        )

    def listar_por_estabelecimento(
        self,
        empresa_id,
        filial_id,
    ):

        return self.repository.listar_por_estabelecimento(
            empresa_id,
            filial_id,
        )

    # ============================================================
    # BUSCAR COMPETÊNCIA
    # ============================================================

    def buscar_existente(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
    ):

        return self.repository.buscar_existente(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=int(mes),
            ano=int(ano),
        )

    # ============================================================
    # OBTER OU CRIAR AUTOMATICAMENTE
    # ============================================================

    def obter_ou_criar(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
    ):

        self.validar_dados_basicos(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
        )

        mes = int(mes)
        ano = int(ano)

        existente = self.buscar_existente(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
        )

        if existente:

            self.garantir_diretorios(
                empresa_id=empresa_id,
                filial_id=filial_id,
                mes=mes,
                ano=ano,
            )

            return existente

        competencia = self.repository.criar(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
            data_entrega=None,
            data_vencimento=None,
            status="PENDENTE",
        )

        self.garantir_diretorios(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
        )

        return competencia

    # ============================================================
    # CRIAÇÃO MANUAL
    #
    # Mantemos por compatibilidade interna,
    # mas a interface principal não usará mais.
    # ============================================================

    def criar(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
        data_entrega="",
        data_vencimento="",
    ):

        self.validar_dados_basicos(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
        )

        mes = int(mes)
        ano = int(ano)

        data_entrega = (
            data_entrega.strip()
            if data_entrega
            else ""
        )

        data_vencimento = (
            data_vencimento.strip()
            if data_vencimento
            else ""
        )

        if data_entrega:

            self.validar_data(
                data_entrega,
                "Data de entrega",
            )

        if data_vencimento:

            self.validar_data(
                data_vencimento,
                "Data de vencimento",
            )

        existente = self.buscar_existente(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
        )

        if existente:

            return existente

        competencia = self.repository.criar(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
            data_entrega=data_entrega or None,
            data_vencimento=data_vencimento or None,
            status="PENDENTE",
        )

        self.garantir_diretorios(
            empresa_id=empresa_id,
            filial_id=filial_id,
            mes=mes,
            ano=ano,
        )

        return competencia

    # ============================================================
    # DIRETÓRIOS
    # ============================================================

    def garantir_diretorios(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
    ):

        empresa = self.empresa_repository.buscar_por_id(
            empresa_id
        )

        if empresa is None:

            raise ValueError(
                "Empresa não encontrada."
            )

        estabelecimento = (
            self.filial_repository.buscar_por_id(
                filial_id
            )
        )

        if estabelecimento is None:

            raise ValueError(
                "Estabelecimento não encontrado."
            )

        if not empresa.diretorio_base:

            raise ValueError(
                "A empresa não possui diretório base cadastrado."
            )

        return self.directory_manager.criar_estrutura_competencia(
            diretorio_base=empresa.diretorio_base,
            identificacao_estabelecimento=(
                estabelecimento.identificacao
            ),
            mes=mes,
            ano=ano,
        )

    def obter_diretorio_competencia(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
    ):

        empresa = self.empresa_repository.buscar_por_id(
            empresa_id
        )

        if empresa is None:

            raise ValueError(
                "Empresa não encontrada."
            )

        estabelecimento = (
            self.filial_repository.buscar_por_id(
                filial_id
            )
        )

        if estabelecimento is None:

            raise ValueError(
                "Estabelecimento não encontrado."
            )

        if not empresa.diretorio_base:

            raise ValueError(
                "A empresa não possui diretório base cadastrado."
            )

        return self.directory_manager.caminho_competencia(
            diretorio_base=empresa.diretorio_base,
            identificacao_estabelecimento=(
                estabelecimento.identificacao
            ),
            mes=mes,
            ano=ano,
        )

    # ============================================================
    # VALIDAÇÕES
    # ============================================================

    def validar_dados_basicos(
        self,
        empresa_id,
        filial_id,
        mes,
        ano,
    ):

        if not empresa_id:

            raise ValueError(
                "Selecione uma empresa."
            )

        if not filial_id:

            raise ValueError(
                "Selecione um estabelecimento."
            )

        try:

            mes = int(mes)

        except (TypeError, ValueError):

            raise ValueError(
                "Informe um mês válido."
            )

        try:

            ano = int(ano)

        except (TypeError, ValueError):

            raise ValueError(
                "Informe um ano válido."
            )

        if mes < 1 or mes > 12:

            raise ValueError(
                "O mês deve estar entre 1 e 12."
            )

        if ano < 2000 or ano > 2100:

            raise ValueError(
                "Informe um ano válido."
            )

    def validar_data(
        self,
        valor,
        nome_campo,
    ):

        try:

            datetime.strptime(
                valor,
                "%d/%m/%Y",
            )

        except ValueError:

            raise ValueError(
                (
                    f"{nome_campo} deve estar "
                    "no formato DD/MM/AAAA."
                )
            )
