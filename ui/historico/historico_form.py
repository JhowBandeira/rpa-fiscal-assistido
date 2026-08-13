from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

from services.empresa_service import EmpresaService
from services.filial_service import FilialService
from services.competencia_service import CompetenciaService
from services.execution_service import ExecutionService


class HistoricoForm(QWidget):

    def __init__(self):
        super().__init__()

        self.empresa_service = EmpresaService()
        self.filial_service = FilialService()
        self.competencia_service = CompetenciaService()
        self.execution_service = ExecutionService()

        self.setWindowTitle(
            "Histórico e Retomada de Execuções"
        )

        self.resize(
            1100,
            650,
        )

        layout_principal = QVBoxLayout()

        # ==========================================
        # EMPRESA
        # ==========================================

        linha_empresa = QHBoxLayout()

        linha_empresa.addWidget(
            QLabel("Empresa:")
        )

        self.combo_empresa = QComboBox()

        self.combo_empresa.currentIndexChanged.connect(
            self.carregar_estabelecimentos
        )

        linha_empresa.addWidget(
            self.combo_empresa,
            1,
        )

        layout_principal.addLayout(
            linha_empresa
        )

        # ==========================================
        # ESTABELECIMENTO
        # ==========================================

        linha_estabelecimento = QHBoxLayout()

        linha_estabelecimento.addWidget(
            QLabel("Estabelecimento:")
        )

        self.combo_estabelecimento = QComboBox()

        self.combo_estabelecimento.currentIndexChanged.connect(
            self.carregar_competencias
        )

        linha_estabelecimento.addWidget(
            self.combo_estabelecimento,
            1,
        )

        layout_principal.addLayout(
            linha_estabelecimento
        )

        # ==========================================
        # COMPETÊNCIA
        # ==========================================

        linha_competencia = QHBoxLayout()

        linha_competencia.addWidget(
            QLabel("Competência:")
        )

        self.combo_competencia = QComboBox()

        self.combo_competencia.currentIndexChanged.connect(
            self.carregar_execucoes
        )

        linha_competencia.addWidget(
            self.combo_competencia,
            1,
        )

        botao_atualizar = QPushButton(
            "Atualizar"
        )

        botao_atualizar.clicked.connect(
            self.carregar_execucoes
        )

        linha_competencia.addWidget(
            botao_atualizar
        )

        layout_principal.addLayout(
            linha_competencia
        )

        # ==========================================
        # TABELA
        # ==========================================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            8
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Tarefa",
                "Status",
                "Etapa",
                "Item",
                "Início",
                "Fim",
                "Erro",
            ]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabela.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabela.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        layout_principal.addWidget(
            self.tabela
        )

        # ==========================================
        # BOTÕES
        # ==========================================

        linha_botoes = QHBoxLayout()

        self.botao_retomar = QPushButton(
            "Retomar do Ponto"
        )

        self.botao_retomar.clicked.connect(
            self.retomar_execucao
        )

        linha_botoes.addWidget(
            self.botao_retomar
        )

        self.botao_detalhes = QPushButton(
            "Ver Checkpoint"
        )

        self.botao_detalhes.clicked.connect(
            self.ver_checkpoint
        )

        linha_botoes.addWidget(
            self.botao_detalhes
        )

        layout_principal.addLayout(
            linha_botoes
        )

        self.setLayout(
            layout_principal
        )

        self.carregar_empresas()

    # ==========================================
    # EMPRESAS
    # ==========================================

    def carregar_empresas(self):

        self.combo_empresa.blockSignals(
            True
        )

        self.combo_empresa.clear()

        try:

            empresas = (
                self.empresa_service.listar()
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            self.combo_empresa.blockSignals(
                False
            )

            return

        self.combo_empresa.addItem(
            "Selecione uma empresa...",
            None,
        )

        for empresa in empresas:

            texto = (
                f"{empresa.razao_social}"
                f" — {empresa.cnpj}"
            )

            self.combo_empresa.addItem(
                texto,
                empresa.id,
            )

        self.combo_empresa.blockSignals(
            False
        )

        self.carregar_estabelecimentos()

    # ==========================================
    # ESTABELECIMENTOS
    # ==========================================

    def carregar_estabelecimentos(self):

        self.combo_estabelecimento.blockSignals(
            True
        )

        self.combo_estabelecimento.clear()

        empresa_id = (
            self.combo_empresa.currentData()
        )

        if empresa_id is None:

            self.combo_estabelecimento.addItem(
                "Selecione primeiro a empresa",
                None,
            )

            self.combo_estabelecimento.blockSignals(
                False
            )

            self.carregar_competencias()

            return

        try:

            estabelecimentos = (
                self.filial_service
                .listar_por_empresa(
                    empresa_id
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            self.combo_estabelecimento.blockSignals(
                False
            )

            return

        self.combo_estabelecimento.addItem(
            "Selecione um estabelecimento...",
            None,
        )

        for estabelecimento in estabelecimentos:

            tipo = (
                estabelecimento.tipo
                or "FILIAL"
            )

            texto = (
                f"{estabelecimento.identificacao}"
                f" — {tipo}"
                f" — {estabelecimento.uf}"
            )

            self.combo_estabelecimento.addItem(
                texto,
                estabelecimento.id,
            )

        self.combo_estabelecimento.blockSignals(
            False
        )

        self.carregar_competencias()

    # ==========================================
    # COMPETÊNCIAS
    # ==========================================

    def carregar_competencias(self):

        self.combo_competencia.blockSignals(
            True
        )

        self.combo_competencia.clear()

        empresa_id = (
            self.combo_empresa.currentData()
        )

        filial_id = (
            self.combo_estabelecimento.currentData()
        )

        if (
            empresa_id is None
            or filial_id is None
        ):

            self.combo_competencia.addItem(
                "Selecione empresa e estabelecimento",
                None,
            )

            self.combo_competencia.blockSignals(
                False
            )

            self.carregar_execucoes()

            return

        try:

            competencias = (
                self.competencia_service
                .listar_por_estabelecimento(
                    empresa_id,
                    filial_id,
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            self.combo_competencia.blockSignals(
                False
            )

            return

        self.combo_competencia.addItem(
            "Selecione uma competência...",
            None,
        )

        for competencia in competencias:

            texto = (
                f"{competencia.mes:02d}/"
                f"{competencia.ano}"
                f" — {competencia.status}"
            )

            self.combo_competencia.addItem(
                texto,
                competencia.id,
            )

        self.combo_competencia.blockSignals(
            False
        )

        self.carregar_execucoes()

    # ==========================================
    # EXECUÇÕES
    # ==========================================

    def carregar_execucoes(self):

        self.tabela.setRowCount(
            0
        )

        competencia_id = (
            self.combo_competencia.currentData()
        )

        if competencia_id is None:
            return

        try:

            execucoes = (
                self.execution_service
                .listar_por_competencia(
                    competencia_id
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            return

        self.tabela.setRowCount(
            len(execucoes)
        )

        for linha, execucao in enumerate(
            execucoes
        ):

            contexto = (
                self.execution_service
                .obter_contexto_retomada(
                    execucao.id
                )
            )

            step_key = (
                contexto["step_key"]
                or ""
            )

            item_key = (
                contexto["item_key"]
                or ""
            )

            inicio = ""

            if execucao.started_at:
                inicio = execucao.started_at.strftime(
                    "%d/%m/%Y %H:%M:%S"
                )

            fim = ""

            if execucao.finished_at:
                fim = execucao.finished_at.strftime(
                    "%d/%m/%Y %H:%M:%S"
                )

            erro = (
                execucao.last_error
                or ""
            )

            valores = [
                str(execucao.id),
                execucao.task_name,
                execucao.status,
                step_key,
                item_key,
                inicio,
                fim,
                erro,
            ]

            for coluna, valor in enumerate(
                valores
            ):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(
                        valor
                    ),
                )

    # ==========================================
    # EXECUÇÃO SELECIONADA
    # ==========================================

    def execution_id_selecionado(self):

        linha = (
            self.tabela.currentRow()
        )

        if linha < 0:
            return None

        item = (
            self.tabela.item(
                linha,
                0,
            )
        )

        if item is None:
            return None

        try:
            return int(
                item.text()
            )

        except ValueError:
            return None

    # ==========================================
    # CHECKPOINT
    # ==========================================

    def ver_checkpoint(self):

        execution_id = (
            self.execution_id_selecionado()
        )

        if execution_id is None:

            QMessageBox.warning(
                self,
                "Nenhuma execução selecionada",
                "Selecione uma execução na tabela.",
            )

            return

        try:

            contexto = (
                self.execution_service
                .obter_contexto_retomada(
                    execution_id
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            return

        if not contexto["possui_checkpoint"]:

            QMessageBox.information(
                self,
                "Checkpoint",
                "Esta execução ainda não possui checkpoint.",
            )

            return

        mensagem = (
            f"Etapa: {contexto['step_key']}\n"
            f"Item: {contexto['item_key']}\n\n"
            f"Dados de retomada:\n"
            f"{contexto['payload']}"
        )

        QMessageBox.information(
            self,
            "Checkpoint da Execução",
            mensagem,
        )

    # ==========================================
    # RETOMAR
    # ==========================================

    def retomar_execucao(self):

        execution_id = (
            self.execution_id_selecionado()
        )

        if execution_id is None:

            QMessageBox.warning(
                self,
                "Nenhuma execução selecionada",
                "Selecione uma execução para retomar.",
            )

            return

        try:

            contexto = (
                self.execution_service
                .obter_contexto_retomada(
                    execution_id
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            return

        if not contexto["possui_checkpoint"]:

            QMessageBox.warning(
                self,
                "Sem checkpoint",
                (
                    "Esta execução não possui "
                    "um ponto salvo para retomada."
                ),
            )

            return

        QMessageBox.information(
            self,
            "Retomada preparada",
            (
                "O ponto de retomada foi localizado.\n\n"
                f"Etapa: {contexto['step_key']}\n"
                f"Item: {contexto['item_key']}\n\n"
                "Quando a rotina operacional estiver ensinada, "
                "o robô continuará exatamente deste ponto."
            ),
        )
