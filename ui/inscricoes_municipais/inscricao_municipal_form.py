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

from services.empresa_service import (
    EmpresaService,
)

from services.filial_service import (
    FilialService,
)

from services.inscricao_municipal_service import (
    InscricaoMunicipalService,
)


class InscricaoMunicipalForm(QWidget):

    inscricao_salva = Signal()

    def __init__(self):
        super().__init__()

        self.empresa_service = (
            EmpresaService()
        )

        self.filial_service = (
            FilialService()
        )

        self.im_service = (
            InscricaoMunicipalService()
        )

        self.setWindowTitle(
            "Cadastro de Inscrições Municipais / CCM"
        )

        self.resize(
            900,
            620,
        )

        layout_principal = (
            QVBoxLayout()
        )

        form = (
            QFormLayout()
        )

        # ==========================================
        # EMPRESA
        # ==========================================

        self.combo_empresa = (
            QComboBox()
        )

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

        self.combo_estabelecimento = (
            QComboBox()
        )

        self.combo_estabelecimento.currentIndexChanged.connect(
            self.estabelecimento_alterado
        )

        form.addRow(
            "Estabelecimento:",
            self.combo_estabelecimento,
        )

        # ==========================================
        # MUNICÍPIO
        # ==========================================

        self.municipio = (
            QLineEdit()
        )

        self.municipio.setPlaceholderText(
            "Ex.: Diadema"
        )

        form.addRow(
            "Município:",
            self.municipio,
        )

        # ==========================================
        # UF
        # ==========================================

        self.combo_uf = (
            QComboBox()
        )

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
        # INSCRIÇÃO MUNICIPAL
        # ==========================================

        self.numero = (
            QLineEdit()
        )

        self.numero.setPlaceholderText(
            "Digite a Inscrição Municipal / CCM"
        )

        form.addRow(
            "Inscrição Municipal / CCM:",
            self.numero,
        )

        # ==========================================
        # ATIVA
        # ==========================================

        self.ativa = (
            QCheckBox(
                "Inscrição ativa"
            )
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

        botao_salvar = (
            QPushButton(
                "Salvar Inscrição Municipal"
            )
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

        self.tabela = (
            QTableWidget()
        )

        self.tabela.setColumnCount(
            4
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Município",
                "UF",
                "Inscrição Municipal / CCM",
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

            self.limpar_dados_estabelecimento()
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

        self.limpar_dados_estabelecimento()
        self.carregar_inscricoes()

    # ==========================================
    # ESTABELECIMENTO ALTERADO
    # ==========================================

    def estabelecimento_alterado(self):

        estabelecimento_id = (
            self.combo_estabelecimento.currentData()
        )

        if estabelecimento_id is None:

            self.limpar_dados_estabelecimento()
            self.carregar_inscricoes()

            return

        try:

            estabelecimento = (
                self.filial_service.repository
                .buscar_por_id(
                    estabelecimento_id
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                (
                    "Não foi possível carregar "
                    "os dados do estabelecimento.\n\n"
                    f"{erro}"
                ),
            )

            return

        if estabelecimento is None:
            return

        if estabelecimento.municipio:

            self.municipio.setText(
                estabelecimento.municipio
            )

        else:

            self.municipio.clear()

        indice_uf = (
            self.combo_uf.findText(
                estabelecimento.uf
            )
        )

        if indice_uf >= 0:

            self.combo_uf.setCurrentIndex(
                indice_uf
            )

        self.carregar_inscricoes()

    # ==========================================
    # LISTAR INSCRIÇÕES
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
                self.im_service
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
                    "as inscrições municipais.\n\n"
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
                    inscricao.municipio
                ),
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    inscricao.uf
                ),
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    inscricao.numero
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
                self.im_service.criar(
                    empresa_id=empresa_id,
                    filial_id=filial_id,
                    municipio=self.municipio.text(),
                    uf=self.combo_uf.currentText(),
                    numero=self.numero.text(),
                    ativa=self.ativa.isChecked(),
                )
            )

            QMessageBox.information(
                self,
                "Sucesso",
                (
                    "Inscrição Municipal / CCM "
                    f"{inscricao.numero} "
                    "cadastrada com sucesso."
                ),
            )

            self.inscricao_salva.emit()

            self.numero.clear()

            self.ativa.setChecked(
                True
            )

            self.carregar_inscricoes()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    def limpar_dados_estabelecimento(self):

        self.municipio.clear()

        self.combo_uf.setCurrentIndex(
            0
        )
