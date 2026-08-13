from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QHBoxLayout,
)

from PySide6.QtCore import Signal

from services.empresa_service import EmpresaService


class EmpresaForm(QWidget):

    empresa_salva = Signal()

    def __init__(self):
        super().__init__()

        self.service = EmpresaService()

        self.setWindowTitle("Cadastro de Empresa")
        self.resize(600, 350)

        layout_principal = QVBoxLayout()

        form = QFormLayout()

        self.razao_social = QLineEdit()
        self.nome_fantasia = QLineEdit()
        self.cnpj = QLineEdit()
        self.diretorio_base = QLineEdit()

        form.addRow(
            "Razão Social:",
            self.razao_social,
        )

        form.addRow(
            "Nome Fantasia:",
            self.nome_fantasia,
        )

        form.addRow(
            "CNPJ:",
            self.cnpj,
        )

        diretorio_layout = QHBoxLayout()

        diretorio_layout.addWidget(
            self.diretorio_base
        )

        botao_diretorio = QPushButton(
            "Selecionar pasta"
        )

        botao_diretorio.clicked.connect(
            self.selecionar_diretorio
        )

        diretorio_layout.addWidget(
            botao_diretorio
        )

        form.addRow(
            "Diretório Base:",
            diretorio_layout,
        )

        layout_principal.addLayout(
            form
        )

        botao_salvar = QPushButton(
            "Salvar Empresa"
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

    def selecionar_diretorio(self):

        diretorio = QFileDialog.getExistingDirectory(
            self,
            "Selecionar diretório base da empresa",
        )

        if diretorio:
            self.diretorio_base.setText(
                diretorio
            )

    def salvar(self):

        try:

            empresa = self.service.criar(
                razao_social=self.razao_social.text(),
                nome_fantasia=self.nome_fantasia.text(),
                cnpj=self.cnpj.text(),
                diretorio_base=self.diretorio_base.text(),
            )

            QMessageBox.information(
                self,
                "Sucesso",
                (
                    f"Empresa '{empresa.razao_social}' "
                    "cadastrada com sucesso."
                ),
            )

            self.empresa_salva.emit()

            self.limpar_campos()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    def limpar_campos(self):

        self.razao_social.clear()
        self.nome_fantasia.clear()
        self.cnpj.clear()
        self.diretorio_base.clear()
