from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
)

from PySide6.QtCore import Signal

from services.empresa_service import (
    EmpresaService,
)

from services.filial_service import (
    FilialService,
)


class FilialForm(QWidget):

    filial_salva = Signal()

    def __init__(self):
        super().__init__()

        self.empresa_service = (
            EmpresaService()
        )

        self.filial_service = (
            FilialService()
        )

        self.setWindowTitle(
            "Cadastro de Estabelecimento"
        )

        self.resize(
            650,
            420,
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

        form.addRow(
            "Empresa:",
            self.combo_empresa,
        )

        # ==========================================
        # TIPO
        # ==========================================

        self.tipo = (
            QComboBox()
        )

        self.tipo.addItem(
            "Selecione..."
        )

        self.tipo.addItem(
            "MATRIZ"
        )

        self.tipo.addItem(
            "FILIAL"
        )

        form.addRow(
            "Tipo:",
            self.tipo,
        )

        # ==========================================
        # IDENTIFICAÇÃO
        # ==========================================

        self.identificacao = (
            QLineEdit()
        )

        self.identificacao.setPlaceholderText(
            "Ex.: 0001 - DIADEMA"
        )

        form.addRow(
            "Identificação:",
            self.identificacao,
        )

        # ==========================================
        # CNPJ
        # ==========================================

        self.cnpj = (
            QLineEdit()
        )

        self.cnpj.setPlaceholderText(
            "00.000.000/0000-00"
        )

        form.addRow(
            "CNPJ:",
            self.cnpj,
        )

        # ==========================================
        # UF
        # ==========================================

        self.uf = (
            QComboBox()
        )

        self.uf.addItem(
            "Selecione..."
        )

        self.uf.addItems(
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
            self.uf,
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

        layout_principal.addLayout(
            form
        )

        # ==========================================
        # SALVAR
        # ==========================================

        botao_salvar = (
            QPushButton(
                "Salvar Estabelecimento"
            )
        )

        botao_salvar.clicked.connect(
            self.salvar
        )

        layout_principal.addWidget(
            botao_salvar
        )

        self.setLayout(
            layout_principal
        )

        self.carregar_empresas()

    def carregar_empresas(self):

        self.combo_empresa.clear()

        try:

            empresas = (
                self.empresa_service
                .listar()
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

    def salvar(self):

        try:

            empresa_id = (
                self.combo_empresa
                .currentData()
            )

            estabelecimento = (
                self.filial_service
                .criar(
                    empresa_id=empresa_id,
                    identificacao=self.identificacao.text(),
                    cnpj=self.cnpj.text(),
                    uf=self.uf.currentText(),
                    municipio=self.municipio.text(),
                    tipo=self.tipo.currentText(),
                )
            )

            QMessageBox.information(
                self,
                "Sucesso",
                (
                    f"{estabelecimento.tipo} "
                    f"'{estabelecimento.identificacao}' "
                    "cadastrado com sucesso."
                ),
            )

            self.filial_salva.emit()

            self.limpar_campos()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    def limpar_campos(self):

        self.tipo.setCurrentIndex(
            0
        )

        self.identificacao.clear()

        self.cnpj.clear()

        self.uf.setCurrentIndex(
            0
        )

        self.municipio.clear()
