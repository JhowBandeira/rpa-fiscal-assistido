import os
import re

from rpa.totvs_access import (
    TotvsAccess,
)

from rpa.totvs_navigation import (
    TotvsNavigation,
)

from rpa.sft_navigation import (
    SftNavigation,
)

from rpa.excel_sft import (
    ExcelSft,
)


class SftRunner:

    def __init__(
        self,
        cnpj_estabelecimento: str,
        identificacao_estabelecimento: str,
        mes: int,
        ano: int,
        diretorio_destino: str,
    ):

        self.cnpj_estabelecimento = (
            self._normalizar_cnpj(
                cnpj_estabelecimento
            )
        )

        self.identificacao_estabelecimento = (
            identificacao_estabelecimento
        )

        self.mes = int(mes)
        self.ano = int(ano)

        self.diretorio_destino = (
            diretorio_destino
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
    # NOME DO ESTABELECIMENTO
    # ========================================================

    def _nome_estabelecimento(
        self,
    ) -> str:

        nome = (
            self.identificacao_estabelecimento
            .upper()
            .strip()
        )

        # Exemplo:
        # 0001 - DIADEMA
        # vira:
        # DIADEMA

        nome = re.sub(
            r"^\d+\s*[-–—]\s*",
            "",
            nome,
        )

        nome = re.sub(
            r'[<>:"/\\|?*]',
            "",
            nome,
        )

        return nome.strip()

    # ========================================================
    # NOME DO ARQUIVO
    # ========================================================

    def nome_arquivo(
        self,
    ) -> str:

        nome = (
            self._nome_estabelecimento()
        )

        competencia = (
            f"{self.mes:02d}"
            f"{self.ano:04d}"
        )

        return (
            f"SFT {nome} "
            f"{competencia}.xlsx"
        )

    # ========================================================
    # CAMINHO FINAL
    # ========================================================

    def caminho_final(
        self,
    ) -> str:

        return os.path.join(
            self.diretorio_destino,
            self.nome_arquivo(),
        )

    # ========================================================
    # VALIDAÇÃO
    # ========================================================

    def validar(
        self,
    ):

        if (
            len(self.cnpj_estabelecimento)
            != 14
        ):

            raise ValueError(
                (
                    "O CNPJ do estabelecimento "
                    "é inválido."
                )
            )

        if not (
            1 <= self.mes <= 12
        ):

            raise ValueError(
                "Competência inválida."
            )

        if self.ano < 2000:

            raise ValueError(
                "Ano da competência inválido."
            )

        if not self.diretorio_destino:

            raise ValueError(
                (
                    "O diretório de destino "
                    "do SFT não foi informado."
                )
            )

    # ========================================================
    # EXECUÇÃO COMPLETA DO SFT
    # ========================================================

    def executar(
        self,
    ):

        self.validar()

        page = (
            self.totvs.fazer_login()
        )

        navegacao_base = (
            TotvsNavigation(
                page
            )
        )

        sft = (
            SftNavigation(
                page
            )
        )

        # ====================================================
        # TELA INICIAL DO TOTVS
        # ====================================================

        page.wait_for_timeout(
            3000
        )

        navegacao_base.aguardar_texto(
            "Filial",
            timeout_ms=30000,
        )

        navegacao_base.aguardar_texto(
            "Ambiente",
            timeout_ms=30000,
        )

        # ====================================================
        # FILIAL
        # ====================================================

        navegacao_base.clicar_lupa_campo(
            "Filial"
        )

        navegacao_base.selecionar_filial_por_cnpj(
            self.cnpj_estabelecimento
        )

        # ====================================================
        # AMBIENTE 9 - LIVROS FISCAIS
        # ====================================================

        navegacao_base.clicar_lupa_campo(
            "Ambiente"
        )

        navegacao_base.selecionar_ambiente_livros_fiscais()

        navegacao_base.entrar_no_ambiente()

        # ====================================================
        # CONSULTAS > CADASTROS > GENÉRICOS
        # ====================================================

        sft.abrir_consultas()

        sft.abrir_cadastros()

        sft.abrir_genericos()

        # ====================================================
        # SFT
        # ====================================================

        sft.pesquisar_sft()

        # ====================================================
        # FILTRO
        # ====================================================

        sft.abrir_filtro()

        data_inicial, data_final = (
            sft.criar_filtro_competencia(
                self.mes,
                self.ano,
            )
        )

        sft.configurar_filtro_criado()

        # ====================================================
        # DICIONÁRIO
        # ====================================================

        sft.abrir_dicionario()

        sft.marcar_todos_dicionario()

        # ====================================================
        # EXPORTAÇÃO
        # ====================================================

        sft.exportar_csv_xml_excel()

        # ====================================================
        # EXCEL
        # ====================================================

        excel = ExcelSft()

        excel.aguardar_excel_temporario(
            timeout_segundos=90
        )

        caminho = (
            excel.salvar_como_xlsx(
                self.caminho_final()
            )
        )

        return {
            "sucesso": True,
            "arquivo": caminho,
            "data_inicial": data_inicial,
            "data_final": data_final,
            "mensagem": (
                "SFT exportado e salvo "
                "com sucesso."
            ),
        }

    # ========================================================
    # FECHAR NAVEGADOR
    # ========================================================

    def fechar(
        self,
    ):

        self.totvs.fechar()
