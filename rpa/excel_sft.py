import os
import time

import win32com.client


class ExcelSft:

    FORMATO_XLSX = 51

    def __init__(
        self,
    ):

        self.excel = None
        self.workbook = None

    # ========================================================
    # CONECTAR AO EXCEL
    # ========================================================

    def aguardar_excel_temporario(
        self,
        timeout_segundos: int = 60,
    ):

        inicio = time.time()

        ultimo_erro = None

        while (
            time.time() - inicio
            < timeout_segundos
        ):

            try:

                excel = (
                    win32com.client.GetActiveObject(
                        "Excel.Application"
                    )
                )

                if excel is None:

                    time.sleep(
                        1
                    )

                    continue

                quantidade = (
                    excel.Workbooks.Count
                )

                if quantidade == 0:

                    time.sleep(
                        1
                    )

                    continue

                # =============================================
                # PROCURA WORKBOOK DO TEMP / XML
                # =============================================

                for indice in range(
                    1,
                    quantidade + 1,
                ):

                    workbook = (
                        excel.Workbooks(
                            indice
                        )
                    )

                    try:

                        caminho = str(
                            workbook.FullName
                        )

                    except Exception:

                        caminho = ""

                    nome = str(
                        workbook.Name
                    )

                    caminho_minusculo = (
                        caminho.lower()
                    )

                    nome_minusculo = (
                        nome.lower()
                    )

                    if (
                        "\\temp\\" in caminho_minusculo
                        or nome_minusculo.endswith(
                            ".xml"
                        )
                    ):

                        self.excel = excel
                        self.workbook = workbook

                        return workbook

                # =============================================
                # FALLBACK:
                # workbook ativo
                # =============================================

                workbook = (
                    excel.ActiveWorkbook
                )

                if workbook is not None:

                    self.excel = excel
                    self.workbook = workbook

                    return workbook

            except Exception as erro:

                ultimo_erro = erro

            time.sleep(
                1
            )

        raise RuntimeError(
            (
                "O TOTVS solicitou a exportação, "
                "mas o Excel não foi localizado "
                "dentro do tempo esperado.\n\n"
                f"Último erro: {ultimo_erro}"
            )
        )

    # ========================================================
    # SALVAR COMO XLSX
    # ========================================================

    def salvar_como_xlsx(
        self,
        caminho_destino: str,
    ):

        if self.workbook is None:

            raise RuntimeError(
                (
                    "Nenhuma planilha do SFT "
                    "está aberta no Excel."
                )
            )

        diretorio = os.path.dirname(
            caminho_destino
        )

        os.makedirs(
            diretorio,
            exist_ok=True,
        )

        caminho_destino = os.path.abspath(
            caminho_destino
        )

        # ====================================================
        # SE EXISTIR, REMOVE ANTES
        # ====================================================

        if os.path.exists(
            caminho_destino
        ):

            os.remove(
                caminho_destino
            )

        # ====================================================
        # DESATIVA AVISOS DO EXCEL
        # ====================================================

        if self.excel is not None:

            try:

                self.excel.DisplayAlerts = False

            except Exception:
                pass

        try:

            self.workbook.SaveAs(
                Filename=caminho_destino,
                FileFormat=self.FORMATO_XLSX,
            )

        finally:

            if self.excel is not None:

                try:

                    self.excel.DisplayAlerts = True

                except Exception:
                    pass

        # ====================================================
        # VALIDAÇÃO
        # ====================================================

        if not os.path.exists(
            caminho_destino
        ):

            raise RuntimeError(
                (
                    "O Excel executou o SaveAs, "
                    "mas o arquivo final não foi "
                    "encontrado."
                )
            )

        tamanho = os.path.getsize(
            caminho_destino
        )

        if tamanho <= 0:

            raise RuntimeError(
                "O arquivo SFT salvo está vazio."
            )

        return caminho_destino
