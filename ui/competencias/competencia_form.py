from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
)

from PySide6.QtCore import Signal

from services.empresa_service import (
    EmpresaService,
)

from services.filial_service import (
    FilialService,
)

from services.competencia_service import (
    CompetenciaService,
)


class CompetenciaForm(QWidget):

    competencia_salva = Signal()

    def __init__(self):
        super().__init__()

        self.empresa_service = (
            EmpresaService()
        )

        self.filial_service = (
            FilialService()
        )

        self.competencia_service = (
            CompetenciaService()
        )

        self.setWindowTitle(
            "Cadastro de Competências"
        )

        self.resize(
            950,
            680,
        )

        layout_principal = (
            QVBoxLayout()
        )

        form = (
            QFormLayout()
        )

        # EMPRESA

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

        # ESTABELECIMENTO

        self.combo_estabelecimento = (
            QComboBox()
        )

        self.combo_estabelecimento.currentIndexChanged.connect(
            self.carregar_competencias
        )

        form.addRow(
            "Estabelecimento:",
            self.combo_estabelecimento,
        )

        # MÊS

        self.mes = (
            QComboBox()
        )

        self.mes.addItem(
            "Selecione..."
        )

        for numero in range(
            1,
            13,
        ):

            self.mes.addItem(
                f"{numero:02d}",
                numero,
            )

        form.addRow(
            "Mês:",
            self.mes,
        )

        # ANO

        self.ano = (
            QSpinBox()
        )

        self.ano.setRange(
            2000,
            2100,
        )

        self.ano.setValue(
            2026
        )

        form.addRow(
            "Ano:",
            self.ano,
        )

        # ENTREGA

        self.data_entrega = (
            QLineEdit()
        )

        self.data_entrega.setPlaceholderText(
            "DD/MM/AAAA"
        )

        form.addRow(
            "Data de entrega:",
            self.data_entrega,
        )

        # VENCIMENTO

        self.data_vencimento = (
            QLineEdit()
        )

        self.data_vencimento.setPlaceholderText(
            "DD/MM/AAAA"
        )

        form.addRow(
            "Data de vencimento:",
            self.data_vencimento,
        )

        layout_principal.addLayout(
            form
        )

        # SALVAR

        botao_salvar = (
            QPushButton(
                "Salvar Competência e Criar Diretórios"
            )
        )

        botao_salvar.clicked.connect(
            self.salvar
        )

        layout_principal.addWidget(
            botao_salvar
        )

        # DIRETÓRIO

        self.label_diretorio = (
            QLabel(
                "Diretório: ainda não criado."
            )
        )

        self.label_diretorio.setWordWrap(
            True
        )

        layout_principal.addWidget(
            self.label_diretorio
        )

        # TABELA

        self.tabela = (
            QTableWidget()
        )

        self.tabela.setColumnCount(
            5
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Competência",
                "Entrega",
                "Vencimento",
                "Status",
                "ID",
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

    def carregar_empresas(self):

        self.combo_empresa.blockSignals(
            True
        )

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

    def carregar_estabelecimentos(self):

        self.combo_estabelecimento.blockSignals(
            True
        )

        self.combo_estabelecimento.clear()

        empresa_id = (
            self.combo_empresa
            .currentData()
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

    def carregar_competencias(self):

        self.tabela.setRowCount(
            0
        )

        empresa_id = (
            self.combo_empresa
            .currentData()
        )

        filial_id = (
            self.combo_estabelecimento
            .currentData()
        )

        if (
            empresa_id is None
            or filial_id is None
        ):

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

            return

        self.tabela.setRowCount(
            len(competencias)
        )

        for linha, competencia in enumerate(
            competencias
        ):

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    f"{competencia.mes:02d}/"
                    f"{competencia.ano}"
                ),
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    competencia.data_entrega
                    or ""
                ),
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    competencia.data_vencimento
                    or ""
                ),
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(
                    competencia.status
                ),
            )

            self.tabela.setItem(
                linha,
                4,
                QTableWidgetItem(
                    str(
                        competencia.id
                    )
                ),
            )

    def salvar(self):

        try:

            empresa_id = (
                self.combo_empresa
                .currentData()
            )

            filial_id = (
                self.combo_estabelecimento
                .currentData()
            )

            mes = (
                self.mes.currentData()
            )

            if mes is None:

                raise ValueError(
                    "Selecione o mês."
                )

            ano = (
                self.ano.value()
            )

            competencia = (
                self.competencia_service
                .criar(
                    empresa_id=empresa_id,
                    filial_id=filial_id,
                    mes=mes,
                    ano=ano,
                    data_entrega=self.data_entrega.text(),
                    data_vencimento=self.data_vencimento.text(),
                )
            )

            diretorio = (
                self.competencia_service
                .obter_diretorio_competencia(
                    empresa_id=empresa_id,
                    filial_id=filial_id,
                    mes=mes,
                    ano=ano,
                )
            )

            self.label_diretorio.setText(
                f"Diretório: {diretorio}"
            )

            QMessageBox.information(
                self,
                "Sucesso",
                (
                    "Competência "
                    f"{competencia.mes:02d}/"
                    f"{competencia.ano} "
                    "cadastrada.\n\n"
                    "Estrutura de diretórios criada "
                    "com sucesso."
                ),
            )

            self.competencia_salva.emit()

            self.limpar_campos()

            self.carregar_competencias()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    def limpar_campos(self):

        self.mes.setCurrentIndex(
            0
        )

        self.data_entrega.clear()

        self.data_vencimento.clear()
