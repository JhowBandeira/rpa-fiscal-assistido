import threading
import time

from PySide6.QtCore import (
    QThread,
    Signal,
)

from rpa.fechar_periodo_runner import (
    FecharPeriodoRunner,
)


class FecharPeriodoWorker(QThread):

    sucesso = Signal(dict)
    erro = Signal(str)
    finalizado = Signal()

    def __init__(
        self,
        cnpj_estabelecimento: str,
        mes: int,
        ano: int,
    ):
        super().__init__()

        self.cnpj_estabelecimento = (
            cnpj_estabelecimento
        )

        self.mes = int(
            mes
        )

        self.ano = int(
            ano
        )

        self._parar = threading.Event()

    # ========================================================
    # EXECUÇÃO
    # ========================================================

    def run(self):

        runner = None

        try:

            runner = (
                FecharPeriodoRunner(
                    cnpj_estabelecimento=(
                        self.cnpj_estabelecimento
                    ),
                    mes=self.mes,
                    ano=self.ano,
                )
            )

            resultado = (
                runner.executar_teste_seguro()
            )

            self.sucesso.emit(
                resultado
            )

            # =================================================
            # MANTÉM A THREAD ATIVA
            #
            # O navegador fica aberto para conferência.
            # =================================================

            while not self._parar.is_set():

                time.sleep(
                    0.2
                )

        except Exception as erro:

            self.erro.emit(
                str(erro)
            )

        finally:

            # =================================================
            # FECHA O PLAYWRIGHT NA MESMA THREAD
            # =================================================

            if runner is not None:

                try:

                    runner.fechar()

                except Exception:
                    pass

            self.finalizado.emit()

    # ========================================================
    # SOLICITAR PARADA
    # ========================================================

    def solicitar_parada(self):

        self._parar.set()
