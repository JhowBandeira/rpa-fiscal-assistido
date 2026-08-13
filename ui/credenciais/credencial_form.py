from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from services.empresa_service import (
    EmpresaService,
)

from services.filial_service import (
    FilialService,
)

from services.credencial_service import (
    CredencialService,
)


class CredencialForm(QWidget):

    def __init__(self):
        super().__init__()

        self.empresa_service = (
            EmpresaService()
        )

        self.filial_service = (
            FilialService()
        )

        self.credencial_service = (
            CredencialService()
        )

        self.setWindowTitle(
            "Cadastro de Credenciais"
        )

        self.resize(
            900,
            650,
        )

        layout = QVBoxLayout()

        form = QFormLayout()

        # ====================================================
        # SISTEMA
        # ====================================================

        self.combo_sistema = QComboBox()

        self.combo_sistema.addItem(
            "Selecione..."
        )

        self.combo_sistema.addItem(
            "TOTVS"
        )

        self.combo_sistema.addItem(
            "GISS ONLINE"
        )

        self.combo_sistema.currentIndexChanged.connect(
            self.sistema_alterado
        )

        form.addRow(
            "Sistema:",
            self.combo_sistema,
        )

        # ====================================================
        # TIPO DE VÍNCULO
        # ====================================================

        self.combo_tipo = QComboBox()

        self.combo_tipo.addItem(
            "GLOBAL",
            "GLOBAL",
        )

        self.combo_tipo.addItem(
            "ESTABELECIMENTO",
            "ESTABELECIMENTO",
        )

        self.combo_tipo.currentIndexChanged.connect(
            self.atualizar_vinculo
        )

        form.addRow(
            "Tipo de vínculo:",
            self.combo_tipo,
        )

        # ====================================================
        # EMPRESA
        # ====================================================

        self.combo_empresa = QComboBox()

        self.combo_empresa.currentIndexChanged.connect(
            self.carregar_estabelecimentos
        )

        form.addRow(
            "Empresa:",
            self.combo_empresa,
        )

        # ====================================================
        # ESTABELECIMENTO
        # ====================================================

        self.combo_estabelecimento = QComboBox()

        form.addRow(
            "Estabelecimento:",
            self.combo_estabelecimento,
        )

        # ====================================================
        # USUÁRIO
        # ====================================================

        self.usuario = QLineEdit()

        self.usuario.setPlaceholderText(
            "Login, usuário ou CPF"
        )

        form.addRow(
            "Usuário / CPF:",
            self.usuario,
        )

        # ====================================================
        # SENHA
        # ====================================================

        self.senha = QLineEdit()

        self.senha.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.senha.setPlaceholderText(
            "Senha"
        )

        form.addRow(
            "Senha:",
            self.senha,
        )

        layout.addLayout(
            form
        )

        # ====================================================
        # SALVAR
        # ====================================================

        botao_salvar = QPushButton(
            "Salvar Credencial"
        )

        botao_salvar.clicked.connect(
            self.salvar
        )

        layout.addWidget(
            botao_salvar
        )

        # ====================================================
        # TABELA
        # ====================================================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            5
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Sistema",
                "Vínculo",
                "Empresa ID",
                "Estabelecimento ID",
                "Usuário",
            ]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(
            self.tabela
        )

        self.setLayout(
            layout
        )

        self.carregar_empresas()
        self.sistema_alterado()
        self.carregar_lista()

    # ========================================================
    # SISTEMA
    # ========================================================

    def sistema_alterado(self):

        sistema = (
            self.combo_sistema.currentText()
        )

        if sistema == "TOTVS":

            indice = (
                self.combo_tipo.findData(
                    "GLOBAL"
                )
            )

            self.combo_tipo.setCurrentIndex(
                indice
            )

            self.combo_tipo.setEnabled(
                False
            )

        elif sistema == "GISS ONLINE":

            indice = (
                self.combo_tipo.findData(
                    "ESTABELECIMENTO"
                )
            )

            self.combo_tipo.setCurrentIndex(
                indice
            )

            self.combo_tipo.setEnabled(
                False
            )

        else:

            self.combo_tipo.setEnabled(
                True
            )

        self.atualizar_vinculo()

    # ========================================================
    # EMPRESAS
    # ========================================================

    def carregar_empresas(self):

        self.combo_empresa.blockSignals(
            True
        )

        self.combo_empresa.clear()

        self.combo_empresa.addItem(
            "Selecione uma empresa...",
            None,
        )

        try:

            empresas = (
                self.empresa_service.listar()
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

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

        self.combo_empresa.blockSignals(
            False
        )

        self.carregar_estabelecimentos()

    # ========================================================
    # ESTABELECIMENTOS
    # ========================================================

    def carregar_estabelecimentos(self):

        self.combo_estabelecimento.clear()

        empresa_id = (
            self.combo_empresa.currentData()
        )

        if empresa_id is None:

            self.combo_estabelecimento.addItem(
                "Selecione primeiro a empresa",
                None,
            )

            return

        try:

            estabelecimentos = (
                self.filial_service
                .listar_por_empresa(
                    empresa_id
                )
            )

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

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    # ========================================================
    # VÍNCULO
    # ========================================================

    def atualizar_vinculo(self):

        tipo = (
            self.combo_tipo.currentData()
        )

        vinculado = (
            tipo
            == "ESTABELECIMENTO"
        )

        self.combo_empresa.setEnabled(
            vinculado
        )

        self.combo_estabelecimento.setEnabled(
            vinculado
        )

    # ========================================================
    # SALVAR
    # ========================================================

    def salvar(self):

        try:

            sistema = (
                self.combo_sistema
                .currentText()
            )

            if sistema == "Selecione...":

                raise ValueError(
                    "Selecione o sistema."
                )

            tipo = (
                self.combo_tipo
                .currentData()
            )

            empresa_id = (
                self.combo_empresa
                .currentData()
            )

            filial_id = (
                self.combo_estabelecimento
                .currentData()
            )

            credencial = (
                self.credencial_service
                .salvar(
                    sistema=sistema,
                    tipo_vinculo=tipo,
                    usuario=self.usuario.text(),
                    senha=self.senha.text(),
                    empresa_id=empresa_id,
                    filial_id=filial_id,
                )
            )

            QMessageBox.information(
                self,
                "Sucesso",
                (
                    f"Credencial de {credencial.sistema} "
                    "salva com sucesso.\n\n"
                    "A senha foi armazenada no cofre "
                    "do Windows."
                ),
            )

            self.usuario.clear()
            self.senha.clear()

            self.carregar_lista()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    # ========================================================
    # LISTAR
    # ========================================================

    def carregar_lista(self):

        try:

            credenciais = (
                self.credencial_service.listar()
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

            return

        self.tabela.setRowCount(
            len(credenciais)
        )

        for linha, credencial in enumerate(
            credenciais
        ):

            valores = [
                credencial.sistema,
                credencial.tipo_vinculo,
                (
                    str(credencial.empresa_id)
                    if credencial.empresa_id
                    else ""
                ),
                (
                    str(credencial.filial_id)
                    if credencial.filial_id
                    else ""
                ),
                credencial.usuario,
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
