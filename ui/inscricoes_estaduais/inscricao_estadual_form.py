from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from PySide6.QtCore import Signal

from services.empresa_service import EmpresaService
from services.filial_service import FilialService
from services.inscricao_estadual_service import (
    InscricaoEstadualService,
)


class InscricaoEstadualForm(QWidget):

    inscricao_salva = Signal()

    def __init__(self):
        super().__init__()

        self.empresa_service = EmpresaService()
        self.filial_service = FilialService()
        self.ie_service = InscricaoEstadualService()

        self.setWindowTitle(
            "Cadastro de Inscrições Estaduais"
        )

        self.resize(
            900,
            620,
        )

        layout_principal = QVBoxLayout()

        form = QFormLayout()

        # ==========================================
        # EMPRESA
        # ==========================================

        self.combo_empresa = QComboBox()

        self.combo_empresa.currentIndexChanged.connect(
            self.carregar_estabelecimentos
        )

        form.addRow(
            "Empresa:",
            self.combo_empresa,
        )

        # ==========================================
        # ESTABELECIMENTO
        # ==========================================

        self.combo_estabelecimento = QComboBox()

        self.combo_estabelecimento.currentIndexChanged.connect(
            self.carregar_inscricoes
        )

        form.addRow(
            "Estabelecimento:",
            self.combo_estabelecimento,
        )

        # ==========================================
        # UF
        # ==========================================

        self.combo_uf = QComboBox()

        self.combo_uf.addItem(
            "Selecione..."
        )

        self.combo_uf.addItems(
            [
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
            ]
        )

        form.addRow(
            "UF:",
            self.combo_uf,
        )

        # ==========================================
        # INSCRIÇÃO ESTADUAL
        # ==========================================

        self.numero = QLineEdit()

        self.numero.setPlaceholderText(
            "Digite a Inscrição Estadual"
        )

        form.addRow(
            "Inscrição Estadual:",
            self.numero,
        )

        # ==========================================
        # EMITIR CND
        # ==========================================

        self.emitir_cnd = QCheckBox(
            "Usar esta inscrição para emissão de CND"
        )

        self.emitir_cnd.setChecked(
            True
        )

        form.addRow(
            "CND:",
            self.emitir_cnd,
        )

        # ==========================================
        # ATIVA
        # ==========================================

        self.ativa = QCheckBox(
            "Inscrição ativa"
        )

        self.ativa.setChecked(
            True
        )

        form.addRow(
            "Status:",
            self.ativa,
        )

        layout_principal.addLayout(
            form
        )

        # ==========================================
        # SALVAR
        # ==========================================

        botao_salvar = QPushButton(
            "Salvar Inscrição Estadual"
        )

        botao_salvar.clicked.connect(
            self.salvar
        )

        layout_principal.addWidget(
            botao_salvar
        )

        # ==========================================
        # TABELA
        # ==========================================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            4
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "UF",
                "Inscrição Estadual",
                "CND",
                "Ativa",
            ]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout_principal.addWidget(
            self.tabela
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
                (
                    "Não foi possível carregar "
                    "as empresas.\n\n"
                    f"{erro}"
                ),
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

            self.carregar_inscricoes()

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
                (
                    "Não foi possível carregar "
                    "os estabelecimentos.\n\n"
                    f"{erro}"
                ),
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
                f" — {estabelecimento.cnpj}"
                f" — {estabelecimento.uf}"
            )

            self.combo_estabelecimento.addItem(
                texto,
                estabelecimento.id,
            )

        self.combo_estabelecimento.blockSignals(
            False
        )

        self.carregar_inscricoes()

    # ==========================================
    # LISTAR IEs
    # ==========================================

    def carregar_inscricoes(self):

        self.tabela.setRowCount(
            0
        )

        filial_id = (
            self.combo_estabelecimento.currentData()
        )

        if filial_id is None:
            return

        try:

            inscricoes = (
                self.ie_service
                .listar_por_estabelecimento(
                    filial_id
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível carregar "
                    "as inscrições estaduais.\n\n"
                    f"{erro}"
                ),
            )

            return

        self.tabela.setRowCount(
            len(inscricoes)
        )

        for linha, inscricao in enumerate(
            inscricoes
        ):

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    inscricao.uf
                ),
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    inscricao.numero
                ),
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    "SIM"
                    if inscricao.emitir_cnd
                    else "NÃO"
                ),
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    "SIM"
                    if inscricao.ativa
                    else "NÃO"
                ),
            )

    # ==========================================
    # SALVAR
    # ==========================================

    def salvar(self):

        try:

            empresa_id = (
                self.combo_empresa.currentData()
            )

            filial_id = (
                self.combo_estabelecimento.currentData()
            )

            inscricao = (
                self.ie_service.criar(
                    empresa_id=empresa_id,
                    filial_id=filial_id,
                    uf=self.combo_uf.currentText(),
                    numero=self.numero.text(),
                    emitir_cnd=self.emitir_cnd.isChecked(),
                    ativa=self.ativa.isChecked(),
                )
            )

            QMessageBox.information(
                self,
                "Sucesso",
                (
                    f"Inscrição Estadual "
                    f"{inscricao.numero} "
                    "cadastrada com sucesso."
                ),
            )

            self.inscricao_salva.emit()

            self.limpar_campos()

            self.carregar_inscricoes()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    def limpar_campos(self):

        self.combo_uf.setCurrentIndex(
            0
        )

        self.numero.clear()

        self.emitir_cnd.setChecked(
            True
        )

        self.ativa.setChecked(
            True
        )
