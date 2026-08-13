import pythoncom

from PySide6.QtCore import (
    QThread,
    Signal,
)

from rpa.sft_runner import (
    SftRunner,
)


class SftWorker(QThread):

    sucesso = Signal(dict)
    erro = Signal(str)
    finalizado = Signal()

    def __init__(
        self,
        cnpj_estabelecimento: str,
        identificacao_estabelecimento: str,
        mes: int,
        ano: int,
        diretorio_destino: str,
    ):
        super().__init__()

        self.cnpj_estabelecimento = (
            cnpj_estabelecimento
        )

        self.identificacao_estabelecimento = (
            identificacao_estabelecimento
        )

        self.mes = int(
            mes
        )

        self.ano = int(
            ano
        )

        self.diretorio_destino = (
            diretorio_destino
        )

    # ========================================================
    # EXECUÇÃO
    # ========================================================

    def run(self):

        runner = None

        # ====================================================
        # NECESSÁRIO PARA AUTOMAÇÃO DO EXCEL
        # DENTRO DE QTHREAD
        # ====================================================

        pythoncom.CoInitialize()

        try:

            runner = (
                SftRunner(
                    cnpj_estabelecimento=(
                        self.cnpj_estabelecimento
                    ),
                    identificacao_estabelecimento=(
                        self.identificacao_estabelecimento
                    ),
                    mes=self.mes,
                    ano=self.ano,
                    diretorio_destino=(
                        self.diretorio_destino
                    ),
                )
            )

            resultado = (
                runner.executar()
            )

            self.sucesso.emit(
                resultado
            )

        except Exception as erro:

            self.erro.emit(
                str(erro)
            )

        finally:

            if runner is not None:

                try:

                    runner.fechar()

                except Exception:
                    pass

            try:

                pythoncom.CoUninitialize()

            except Exception:
                pass

            self.finalizado.emit()
