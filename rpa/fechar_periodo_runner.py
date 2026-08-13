import calendar

from rpa.totvs_access import (
    TotvsAccess,
)

from rpa.totvs_navigation import (
    TotvsNavigation,
)


class FecharPeriodoRunner:

    def __init__(
        self,
        cnpj_estabelecimento: str,
        mes: int,
        ano: int,
    ):

        self.cnpj_estabelecimento = (
            self._normalizar_cnpj(
                cnpj_estabelecimento
            )
        )

        self.mes = int(
            mes
        )

        self.ano = int(
            ano
        )

        self.totvs = TotvsAccess()

    # ========================================================
    # CNPJ
    # ========================================================

    def _normalizar_cnpj(
        self,
        cnpj: str,
    ) -> str:

        return (
            str(cnpj)
            .replace(".", "")
            .replace("/", "")
            .replace("-", "")
            .replace(" ", "")
            .strip()
        )

    # ========================================================
    # VALIDAÇÃO
    # ========================================================

    def validar(self):

        if (
            len(self.cnpj_estabelecimento)
            != 14
        ):

            raise ValueError(
                (
                    "O estabelecimento selecionado "
                    "não possui um CNPJ válido."
                )
            )

        if not (
            1 <= self.mes <= 12
        ):

            raise ValueError(
                "Mês da competência inválido."
            )

        if self.ano < 2000:

            raise ValueError(
                "Ano da competência inválido."
            )

    # ========================================================
    # ÚLTIMO DIA DA COMPETÊNCIA
    # ========================================================

    def calcular_ultimo_dia_competencia(
        self,
    ) -> str:

        ultimo_dia = (
            calendar.monthrange(
                self.ano,
                self.mes,
            )[1]
        )

        return (
            f"{ultimo_dia:02d}/"
            f"{self.mes:02d}/"
            f"{self.ano:04d}"
        )

    # ========================================================
    # TESTE SEGURO
    #
    # - chega à tela de fechamento
    # - calcula o último dia da competência
    # - preenche Nova data
    # - NÃO clica em OK
    # ========================================================

    def executar_teste_seguro(
        self,
    ):

        self.validar()

        nova_data = (
            self.calcular_ultimo_dia_competencia()
        )

        page = (
            self.totvs.fazer_login()
        )

        navegacao = (
            TotvsNavigation(
                page
            )
        )

        # ====================================================
        # TELA INICIAL
        # ====================================================

        page.wait_for_timeout(
            3000
        )

        navegacao.aguardar_texto(
            "Grupo",
            timeout_ms=30000,
        )

        navegacao.aguardar_texto(
            "Filial",
            timeout_ms=30000,
        )

        navegacao.aguardar_texto(
            "Ambiente",
            timeout_ms=30000,
        )

        # ====================================================
        # FILIAL
        # ====================================================

        navegacao.clicar_lupa_campo(
            "Filial"
        )

        navegacao.selecionar_filial_por_cnpj(
            self.cnpj_estabelecimento
        )

        # ====================================================
        # AMBIENTE
        # ====================================================

        navegacao.clicar_lupa_campo(
            "Ambiente"
        )

        navegacao.selecionar_ambiente_livros_fiscais()

        # ====================================================
        # ENTRAR
        # ====================================================

        navegacao.entrar_no_ambiente()

        # ====================================================
        # MENU
        # ====================================================

        navegacao.abrir_miscelanea()

        navegacao.abrir_acertos()

        # ====================================================
        # DATA FECH/TO FISCAL
        # ====================================================

        navegacao.abrir_data_fechamento_fiscal()

        navegacao.confirmar_tela_fechamento()

        # ====================================================
        # PREENCHE NOVA DATA
        #
        # NÃO CLICA EM OK
        # ====================================================

        navegacao.preencher_nova_data(
            nova_data
        )

        # ====================================================
        # PARADA SEGURA
        # ====================================================

        return {
            "sucesso": True,
            "page": page,
            "cnpj": self.cnpj_estabelecimento,
            "mes": self.mes,
            "ano": self.ano,
            "nova_data": nova_data,
            "mensagem": (
                "O robô chegou à tela de fechamento "
                f"e preencheu a Nova data com {nova_data}, "
                "sem confirmar o fechamento."
            ),
        }

    # ========================================================
    # FECHAR
    # ========================================================

    def fechar(
        self,
    ):

        self.totvs.fechar()
