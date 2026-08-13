import os

from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QFileDialog,
)

from PySide6.QtCore import (
    Qt,
    QSettings,
)

from ui.empresas.empresa_form import (
    EmpresaForm,
)

from ui.filiais.filial_form import (
    FilialForm,
)

from ui.inscricoes_estaduais.inscricao_estadual_form import (
    InscricaoEstadualForm,
)

from ui.inscricoes_municipais.inscricao_municipal_form import (
    InscricaoMunicipalForm,
)

from ui.historico.historico_form import (
    HistoricoForm,
)

from ui.credenciais.credencial_form import (
    CredencialForm,
)

from services.empresa_service import (
    EmpresaService,
)

from services.filial_service import (
    FilialService,
)

from services.competencia_service import (
    CompetenciaService,
)

from services.execution_service import (
    ExecutionService,
)

from workers.fechar_periodo_worker import (
    FecharPeriodoWorker,
)

from workers.sft_worker import (
    SftWorker,
)


# ============================================================
# TAREFAS
# ============================================================

TASKS = [
    {
        "key": "fechar_periodo",
        "name": "Fechar período",
    },
    {
        "key": "salvar_sft",
        "name": "Salvar SFT",
    },
    {
        "key": "apurar_icms",
        "name": "Apurar ICMS",
    },
    {
        "key": "apurar_icms_st_sp",
        "name": "Apurar ICMS-ST SP",
    },
    {
        "key": "gerar_gnre",
        "name": "Gerar GNRE",
    },
    {
        "key": "gerar_dare_sp",
        "name": "Gerar DARE-SP",
    },
    {
        "key": "apurar_ipi",
        "name": "Apurar IPI",
    },
    {
        "key": "apurar_pis",
        "name": "Apurar PIS",
    },
    {
        "key": "apurar_cofins",
        "name": "Apurar COFINS",
    },
    {
        "key": "livro_entrada",
        "name": "Salvar Livro de Entrada",
    },
    {
        "key": "livro_saida",
        "name": "Salvar Livro de Saída",
    },
    {
        "key": "livro_icms",
        "name": "Salvar Livro de ICMS",
    },
    {
        "key": "livro_ipi",
        "name": "Salvar Livro de IPI",
    },
    {
        "key": "servicos_tomados",
        "name": "Salvar Serviços Tomados",
    },
    {
        "key": "servicos_prestados",
        "name": "Salvar Serviços Prestados",
    },
    {
        "key": "pis_cofins",
        "name": "Salvar PIS/COFINS",
    },
    {
        "key": "giss_online",
        "name": "Executar GISS Online",
    },
    {
        "key": "gia_st_3",
        "name": "Executar GIA-ST 3",
    },
    {
        "key": "baixar_cnds",
        "name": "Baixar CNDs",
    },
]


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        # ====================================================
        # FORMS
        # ====================================================

        self.empresa_form = None
        self.filial_form = None
        self.ie_form = None
        self.im_form = None
        self.credencial_form = None
        self.historico_form = None

        # ====================================================
        # SERVICES
        # ====================================================

        self.empresa_service = (
            EmpresaService()
        )

        self.filial_service = (
            FilialService()
        )

        self.competencia_service = (
            CompetenciaService()
        )

        self.execution_service = (
            ExecutionService()
        )

        # ====================================================
        # CONFIGURAÇÕES LOCAIS
        # ====================================================

        self.settings = QSettings(
            "RPAFiscalAssistido",
            "RPAFiscalAssistido",
        )

        # ====================================================
        # CACHE
        # ====================================================

        self.estabelecimentos_cache = {}

        # ====================================================
        # EXECUÇÕES
        # ====================================================

        self.execucoes_atuais = []

        # ====================================================
        # WORKERS
        # ====================================================

        self.fechar_periodo_worker = None
        self.sft_worker = None

        # ====================================================
        # JANELA
        # ====================================================

        self.setWindowTitle(
            "RPA Fiscal Assistido"
        )

        self.resize(
            1180,
            850,
        )

        self.criar_menu()
        self.criar_interface()
        self.carregar_empresas()
        self.atualizar_diretorio_sft_visual()

    # ========================================================
    # MENU
    # ========================================================

    def criar_menu(self):

        barra_menu = self.menuBar()

        # ====================================================
        # CADASTROS
        # ====================================================

        menu_cadastros = (
            barra_menu.addMenu(
                "Cadastros"
            )
        )

        acao_empresas = (
            menu_cadastros.addAction(
                "Empresas"
            )
        )

        acao_empresas.triggered.connect(
            self.abrir_empresas
        )

        acao_estabelecimentos = (
            menu_cadastros.addAction(
                "Estabelecimentos"
            )
        )

        acao_estabelecimentos.triggered.connect(
            self.abrir_filiais
        )

        menu_cadastros.addSeparator()

        acao_ie = (
            menu_cadastros.addAction(
                "Inscrições Estaduais"
            )
        )

        acao_ie.triggered.connect(
            self.abrir_inscricoes_estaduais
        )

        acao_im = (
            menu_cadastros.addAction(
                "Inscrições Municipais / CCM"
            )
        )

        acao_im.triggered.connect(
            self.abrir_inscricoes_municipais
        )

        menu_cadastros.addSeparator()

        acao_credenciais = (
            menu_cadastros.addAction(
                "Credenciais"
            )
        )

        acao_credenciais.triggered.connect(
            self.abrir_credenciais
        )

        # ====================================================
        # CONFIGURAÇÕES
        # ====================================================

        menu_config = (
            barra_menu.addMenu(
                "Configurações"
            )
        )

        acao_diretorio_sft = (
            menu_config.addAction(
                "Diretório do SFT"
            )
        )

        acao_diretorio_sft.triggered.connect(
            self.selecionar_diretorio_sft
        )

        # ====================================================
        # EXECUÇÃO
        # ====================================================

        menu_execucao = (
            barra_menu.addMenu(
                "Execução"
            )
        )

        acao_historico = (
            menu_execucao.addAction(
                "Histórico / Retomar"
            )
        )

        acao_historico.triggered.connect(
            self.abrir_historico
        )

    # ========================================================
    # INTERFACE
    # ========================================================

    def criar_interface(self):

        root = QWidget()

        layout = QVBoxLayout(
            root
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        titulo = QLabel(
            (
                "RPA Fiscal Assistido "
                "— Executor Operacional"
            )
        )

        layout.addWidget(
            titulo
        )

        subtitulo = QLabel(
            (
                "Selecione empresa, estabelecimento, "
                "competência e as tarefas."
            )
        )

        layout.addWidget(
            subtitulo
        )

        # ====================================================
        # EMPRESA
        # ====================================================

        empresa_layout = QHBoxLayout()

        empresa_layout.addWidget(
            QLabel("Empresa:")
        )

        self.combo_empresa = QComboBox()

        self.combo_empresa.currentIndexChanged.connect(
            self.carregar_estabelecimentos
        )

        empresa_layout.addWidget(
            self.combo_empresa,
            1,
        )

        botao_atualizar = QPushButton(
            "Atualizar"
        )

        botao_atualizar.clicked.connect(
            self.carregar_empresas
        )

        empresa_layout.addWidget(
            botao_atualizar
        )

        layout.addLayout(
            empresa_layout
        )

        # ====================================================
        # ESTABELECIMENTO
        # ====================================================

        estabelecimento_layout = QHBoxLayout()

        estabelecimento_layout.addWidget(
            QLabel(
                "Estabelecimento:"
            )
        )

        self.combo_estabelecimento = (
            QComboBox()
        )

        estabelecimento_layout.addWidget(
            self.combo_estabelecimento,
            1,
        )

        layout.addLayout(
            estabelecimento_layout
        )

        # ====================================================
        # COMPETÊNCIA
        # ====================================================

        competencia_layout = QHBoxLayout()

        competencia_layout.addWidget(
            QLabel(
                "Competência:"
            )
        )

        self.combo_mes = QComboBox()

        meses = [
            ("Janeiro", 1),
            ("Fevereiro", 2),
            ("Março", 3),
            ("Abril", 4),
            ("Maio", 5),
            ("Junho", 6),
            ("Julho", 7),
            ("Agosto", 8),
            ("Setembro", 9),
            ("Outubro", 10),
            ("Novembro", 11),
            ("Dezembro", 12),
        ]

        for nome_mes, numero_mes in meses:

            self.combo_mes.addItem(
                (
                    f"{numero_mes:02d} "
                    f"- {nome_mes}"
                ),
                numero_mes,
            )

        competencia_layout.addWidget(
            self.combo_mes
        )

        self.spin_ano = QSpinBox()

        self.spin_ano.setRange(
            2020,
            2100,
        )

        self.spin_ano.setValue(
            datetime.now().year
        )

        competencia_layout.addWidget(
            self.spin_ano
        )

        layout.addLayout(
            competencia_layout
        )

        # ====================================================
        # COMPETÊNCIA VISUAL
        # ====================================================

        self.label_competencia = QLabel(
            "Competência selecionada: -"
        )

        layout.addWidget(
            self.label_competencia
        )

        # ====================================================
        # DIRETÓRIO SFT
        # ====================================================

        diretorio_layout = QHBoxLayout()

        diretorio_layout.addWidget(
            QLabel(
                "Diretório SFT:"
            )
        )

        self.label_diretorio_sft = QLabel(
            "Não configurado"
        )

        diretorio_layout.addWidget(
            self.label_diretorio_sft,
            1,
        )

        self.botao_diretorio_sft = QPushButton(
            "Selecionar pasta"
        )

        self.botao_diretorio_sft.clicked.connect(
            self.selecionar_diretorio_sft
        )

        diretorio_layout.addWidget(
            self.botao_diretorio_sft
        )

        layout.addLayout(
            diretorio_layout
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.label_status = QLabel(
            "Status: aguardando execução."
        )

        layout.addWidget(
            self.label_status
        )

        # ====================================================
        # TAREFAS
        # ====================================================

        self.tasks = QListWidget()

        for tarefa in TASKS:

            item = QListWidgetItem(
                (
                    f"{tarefa['name']} "
                    "— AGUARDANDO_TREINAMENTO"
                )
            )

            item.setCheckState(
                Qt.CheckState.Unchecked
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                tarefa,
            )

            self.tasks.addItem(
                item
            )

        layout.addWidget(
            self.tasks
        )

        # ====================================================
        # TESTE FECHAMENTO
        # ====================================================

        botoes_fechamento = QHBoxLayout()

        self.botao_testar_fechamento = (
            QPushButton(
                (
                    "Testar Fechar período "
                    "— sem confirmar"
                )
            )
        )

        self.botao_testar_fechamento.clicked.connect(
            self.testar_fechar_periodo
        )

        botoes_fechamento.addWidget(
            self.botao_testar_fechamento
        )

        self.botao_encerrar_teste = (
            QPushButton(
                "Encerrar teste seguro"
            )
        )

        self.botao_encerrar_teste.setEnabled(
            False
        )

        self.botao_encerrar_teste.clicked.connect(
            self.encerrar_teste_seguro
        )

        botoes_fechamento.addWidget(
            self.botao_encerrar_teste
        )

        layout.addLayout(
            botoes_fechamento
        )

        # ====================================================
        # EXECUTAR SFT
        # ====================================================

        self.botao_executar_sft = (
            QPushButton(
                "Executar Salvar SFT"
            )
        )

        self.botao_executar_sft.clicked.connect(
            self.executar_sft
        )

        layout.addWidget(
            self.botao_executar_sft
        )

        # ====================================================
        # EXECUÇÃO GERAL
        # ====================================================

        self.botao_executar = QPushButton(
            "Executar selecionadas"
        )

        self.botao_executar.clicked.connect(
            self.executar_selecionadas
        )

        layout.addWidget(
            self.botao_executar
        )

        self.botao_pausar = QPushButton(
            "Pausar"
        )

        self.botao_pausar.clicked.connect(
            self.pausar_execucoes
        )

        layout.addWidget(
            self.botao_pausar
        )

        self.botao_continuar = QPushButton(
            "Continuar"
        )

        self.botao_continuar.clicked.connect(
            self.continuar_execucoes
        )

        layout.addWidget(
            self.botao_continuar
        )

        self.botao_parar = QPushButton(
            "Parar robô"
        )

        self.botao_parar.clicked.connect(
            self.parar_execucoes
        )

        layout.addWidget(
            self.botao_parar
        )

        self.setCentralWidget(
            root
        )

        # ====================================================
        # EVENTOS
        # ====================================================

        self.combo_mes.currentIndexChanged.connect(
            self.atualizar_competencia_visual
        )

        self.spin_ano.valueChanged.connect(
            self.atualizar_competencia_visual
        )

        self.combo_estabelecimento.currentIndexChanged.connect(
            self.atualizar_status_tarefas
        )

        self.atualizar_competencia_visual()

      # ========================================================
    # DIRETÓRIO SFT
    # ========================================================

    def selecionar_diretorio_sft(self):

        diretorio_atual = (
            self.obter_diretorio_sft()
        )

        diretorio = (
            QFileDialog.getExistingDirectory(
                self,
                "Selecione o diretório do SFT",
                diretorio_atual,
            )
        )

        if not diretorio:
            return

        self.settings.setValue(
            "diretorio_sft",
            str(diretorio),
        )

        self.atualizar_diretorio_sft_visual()

    def obter_diretorio_sft(
        self,
    ) -> str:

        valor = self.settings.value(
            "diretorio_sft",
            "",
        )

        if valor is None:
            return ""

        return str(valor)

    def atualizar_diretorio_sft_visual(
        self,
    ):

        diretorio: str = (
            self.obter_diretorio_sft()
        )

        if diretorio:

            self.label_diretorio_sft.setText(
                str(diretorio)
            )

        else:

            self.label_diretorio_sft.setText(
                "Não configurado"
            )

    # ========================================================
    # DIRETÓRIO FINAL DA COMPETÊNCIA
    # ========================================================

    def montar_diretorio_sft_execucao(
        self,
        estabelecimento,
        mes,
        ano,
    ) -> str:

        raiz: str = (
            self.obter_diretorio_sft()
        )

        if not raiz:

            raise RuntimeError(
                (
                    "Configure primeiro "
                    "o Diretório do SFT."
                )
            )

        identificacao: str = str(
            estabelecimento.identificacao
        ).strip()

        mes_numero = int(
            mes
        )

        ano_numero = int(
            ano
        )

        pasta_competencia: str = (
            f"{mes_numero:02d}-"
            f"{ano_numero:04d}"
        )

        diretorio: str = os.path.join(
            str(raiz),
            str(identificacao),
            str(ano_numero),
            str(pasta_competencia),
        )

        os.makedirs(
            diretorio,
            exist_ok=True,
        )

        return diretorio

    # ========================================================
    # COMPETÊNCIA VISUAL
    # ========================================================

    def atualizar_competencia_visual(self):

        mes = self.combo_mes.currentData()
        ano = self.spin_ano.value()

        if mes is None:

            self.label_competencia.setText(
                "Competência selecionada: -"
            )

            return

        self.label_competencia.setText(
            (
                "Competência selecionada: "
                f"{mes:02d}/{ano}"
            )
        )

        self.atualizar_status_tarefas()

    # ========================================================
    # EMPRESAS
    # ========================================================

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

    def empresa_selecionada_id(self):

        return (
            self.combo_empresa.currentData()
        )

    # ========================================================
    # ESTABELECIMENTOS
    # ========================================================

    def carregar_estabelecimentos(self):

        self.combo_estabelecimento.blockSignals(
            True
        )

        self.combo_estabelecimento.clear()

        self.estabelecimentos_cache = {}

        empresa_id = (
            self.empresa_selecionada_id()
        )

        if empresa_id is None:

            self.combo_estabelecimento.addItem(
                "Selecione primeiro a empresa",
                None,
            )

            self.combo_estabelecimento.blockSignals(
                False
            )

            self.atualizar_status_tarefas()

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
                f" — {estabelecimento.cnpj}"
                f" — {estabelecimento.uf}"
            )

            self.combo_estabelecimento.addItem(
                texto,
                estabelecimento.id,
            )

            self.estabelecimentos_cache[
                estabelecimento.id
            ] = estabelecimento

        self.combo_estabelecimento.blockSignals(
            False
        )

        self.atualizar_status_tarefas()

    def estabelecimento_selecionado_id(self):

        return (
            self.combo_estabelecimento.currentData()
        )

    def estabelecimento_selecionado(self):

        estabelecimento_id = (
            self.estabelecimento_selecionado_id()
        )

        if estabelecimento_id is None:
            return None

        return (
            self.estabelecimentos_cache.get(
                estabelecimento_id
            )
        )

    # ========================================================
    # COMPETÊNCIA
    # ========================================================

    def obter_mes_ano(self):

        mes = self.combo_mes.currentData()
        ano = self.spin_ano.value()

        return mes, ano

    def obter_competencia_atual(
        self,
        criar=False,
    ):

        empresa_id = (
            self.empresa_selecionada_id()
        )

        estabelecimento_id = (
            self.estabelecimento_selecionado_id()
        )

        mes, ano = (
            self.obter_mes_ano()
        )

        if (
            empresa_id is None
            or estabelecimento_id is None
            or mes is None
        ):

            return None

        if criar:

            return (
                self.competencia_service
                .obter_ou_criar(
                    empresa_id=empresa_id,
                    filial_id=estabelecimento_id,
                    mes=mes,
                    ano=ano,
                )
            )

        return (
            self.competencia_service
            .buscar_existente(
                empresa_id=empresa_id,
                filial_id=estabelecimento_id,
                mes=mes,
                ano=ano,
            )
        )

    # ========================================================
    # EXECUTAR SFT
    # ========================================================

    def executar_sft(self):

        if (
            self.sft_worker is not None
            and self.sft_worker.isRunning()
        ):

            QMessageBox.warning(
                self,
                "SFT",
                (
                    "Já existe uma rotina "
                    "SFT em execução."
                ),
            )

            return

        estabelecimento = (
            self.estabelecimento_selecionado()
        )

        if estabelecimento is None:

            QMessageBox.warning(
                self,
                "SFT",
                (
                    "Selecione um "
                    "estabelecimento."
                ),
            )

            return

        mes, ano = (
            self.obter_mes_ano()
        )

        if mes is None:

            QMessageBox.warning(
                self,
                "SFT",
                "Selecione a competência.",
            )

            return

        raiz = (
            self.obter_diretorio_sft()
        )

        if not raiz:

            QMessageBox.warning(
                self,
                "Diretório SFT",
                (
                    "Configure primeiro "
                    "o diretório do SFT."
                ),
            )

            return

        try:

            diretorio_destino = (
                self.montar_diretorio_sft_execucao(
                    estabelecimento,
                    mes,
                    ano,
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Diretório SFT",
                str(erro),
            )

            return

        resposta = QMessageBox.question(
            self,
            "Executar SFT",
            (
                "O robô executará o processo "
                "completo do SFT.\n\n"
                f"Estabelecimento: "
                f"{estabelecimento.identificacao}\n"
                f"CNPJ: {estabelecimento.cnpj}\n"
                f"Competência: {mes:02d}/{ano}\n\n"
                f"Destino:\n"
                f"{diretorio_destino}\n\n"
                "Deseja iniciar?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
        )

        if (
            resposta
            != QMessageBox.StandardButton.Yes
        ):

            return

        # ====================================================
        # GARANTE COMPETÊNCIA
        # ====================================================

        try:

            competencia = (
                self.obter_competencia_atual(
                    criar=True
                )
            )

            if competencia is None:

                raise RuntimeError(
                    (
                        "Não foi possível "
                        "preparar a competência."
                    )
                )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Competência",
                str(erro),
            )

            return

        # ====================================================
        # WORKER
        # ====================================================

        self.sft_worker = (
            SftWorker(
                cnpj_estabelecimento=(
                    estabelecimento.cnpj
                ),
                identificacao_estabelecimento=(
                    estabelecimento.identificacao
                ),
                mes=mes,
                ano=ano,
                diretorio_destino=(
                    diretorio_destino
                ),
            )
        )

        self.sft_worker.sucesso.connect(
            self.sft_sucesso
        )

        self.sft_worker.erro.connect(
            self.sft_erro
        )

        self.sft_worker.finalizado.connect(
            self.sft_finalizado
        )

        self.botao_executar_sft.setEnabled(
            False
        )

        self.label_status.setText(
            (
                "Status: executando "
                "Salvar SFT..."
            )
        )

        self.sft_worker.start()

    # ========================================================
    # SFT SUCESSO
    # ========================================================

    def sft_sucesso(
        self,
        resultado,
    ):

        self.label_status.setText(
            "Status: SFT CONCLUÍDO."
        )

        QMessageBox.information(
            self,
            "SFT concluído",
            (
                "SFT exportado com sucesso.\n\n"
                f"Período:\n"
                f"{resultado['data_inicial']} "
                f"até {resultado['data_final']}\n\n"
                f"Arquivo:\n"
                f"{resultado['arquivo']}"
            ),
        )

    # ========================================================
    # SFT ERRO
    # ========================================================

    def sft_erro(
        self,
        mensagem,
    ):

        self.label_status.setText(
            "Status: erro no SFT."
        )

        QMessageBox.critical(
            self,
            "Erro no SFT",
            mensagem,
        )

    # ========================================================
    # SFT FINALIZADO
    # ========================================================

    def sft_finalizado(self):

        self.botao_executar_sft.setEnabled(
            True
        )

        self.sft_worker = None

    # ========================================================
    # TESTE FECHAR PERÍODO
    # ========================================================

    def testar_fechar_periodo(self):

        if (
            self.fechar_periodo_worker is not None
            and self.fechar_periodo_worker.isRunning()
        ):

            QMessageBox.warning(
                self,
                "Teste em andamento",
                (
                    "Já existe um teste seguro "
                    "em execução."
                ),
            )

            return

        estabelecimento = (
            self.estabelecimento_selecionado()
        )

        if estabelecimento is None:

            QMessageBox.warning(
                self,
                "Estabelecimento",
                (
                    "Selecione o estabelecimento "
                    "que deseja testar."
                ),
            )

            return

        mes, ano = (
            self.obter_mes_ano()
        )

        if mes is None:

            QMessageBox.warning(
                self,
                "Competência",
                "Selecione a competência.",
            )

            return

        resposta = QMessageBox.question(
            self,
            "Teste seguro",
            (
                "O robô fará o teste abaixo:\n\n"
                f"Estabelecimento: "
                f"{estabelecimento.identificacao}\n"
                f"CNPJ: {estabelecimento.cnpj}\n"
                f"Competência: {mes:02d}/{ano}\n\n"
                "O robô chegará até a tela "
                "Data Fech/to Fiscal.\n\n"
                "O botão OK NÃO será clicado.\n"
                "Nenhum fechamento será realizado.\n\n"
                "Deseja continuar?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
        )

        if (
            resposta
            != QMessageBox.StandardButton.Yes
        ):

            return

        self.fechar_periodo_worker = (
            FecharPeriodoWorker(
                cnpj_estabelecimento=(
                    estabelecimento.cnpj
                ),
                mes=mes,
                ano=ano,
            )
        )

        self.fechar_periodo_worker.sucesso.connect(
            self.teste_fechamento_sucesso
        )

        self.fechar_periodo_worker.erro.connect(
            self.teste_fechamento_erro
        )

        self.fechar_periodo_worker.finalizado.connect(
            self.teste_fechamento_finalizado
        )

        self.botao_testar_fechamento.setEnabled(
            False
        )

        self.botao_encerrar_teste.setEnabled(
            True
        )

        self.label_status.setText(
            (
                "Status: executando teste "
                "seguro do fechamento..."
            )
        )

        self.fechar_periodo_worker.start()

    # ========================================================
    # FECHAMENTO SUCESSO
    # ========================================================

    def teste_fechamento_sucesso(
        self,
        resultado,
    ):

        self.label_status.setText(
            (
                "Status: teste seguro concluído. "
                "TOTVS aguardando conferência."
            )
        )

        nova_data = (
            resultado.get(
                "nova_data",
                "",
            )
        )

        mensagem_data = ""

        if nova_data:

            mensagem_data = (
                f"\nNova data preenchida: "
                f"{nova_data}\n"
            )

        QMessageBox.information(
            self,
            "Teste concluído",
            (
                f"{resultado['mensagem']}\n"
                f"{mensagem_data}\n"
                "O botão OK NÃO foi clicado.\n"
                "Nenhum fechamento foi realizado.\n\n"
                "Quando terminar a conferência, "
                "clique em 'Encerrar teste seguro'."
            ),
        )

    # ========================================================
    # FECHAMENTO ERRO
    # ========================================================

    def teste_fechamento_erro(
        self,
        mensagem,
    ):

        self.label_status.setText(
            "Status: erro no teste."
        )

        QMessageBox.critical(
            self,
            "Erro no teste",
            mensagem,
        )

    # ========================================================
    # ENCERRAR TESTE
    # ========================================================

    def encerrar_teste_seguro(self):

        if self.fechar_periodo_worker is None:
            return

        if not self.fechar_periodo_worker.isRunning():
            return

        self.botao_encerrar_teste.setEnabled(
            False
        )

        self.label_status.setText(
            (
                "Status: encerrando "
                "teste seguro..."
            )
        )

        self.fechar_periodo_worker.solicitar_parada()

    # ========================================================
    # FECHAMENTO FINALIZADO
    # ========================================================

    def teste_fechamento_finalizado(self):

        self.botao_testar_fechamento.setEnabled(
            True
        )

        self.botao_encerrar_teste.setEnabled(
            False
        )

        self.fechar_periodo_worker = None

    # ========================================================
    # STATUS DAS TAREFAS
    # ========================================================

    def atualizar_status_tarefas(self):

        if not hasattr(
            self,
            "tasks",
        ):
            return

        mapa_status = {}

        try:

            competencia = (
                self.obter_competencia_atual(
                    criar=False
                )
            )

            if competencia is not None:

                execucoes = (
                    self.execution_service
                    .listar_por_competencia(
                        competencia.id
                    )
                )

                for execucao in execucoes:

                    mapa_status[
                        execucao.task_key
                    ] = execucao.status

        except Exception:
            pass

        for indice in range(
            self.tasks.count()
        ):

            item = self.tasks.item(
                indice
            )

            tarefa = item.data(
                Qt.ItemDataRole.UserRole
            )

            status = mapa_status.get(
                tarefa["key"],
                "AGUARDANDO_TREINAMENTO",
            )

            item.setText(
                (
                    f"{tarefa['name']} "
                    f"— {status}"
                )
            )

    # ========================================================
    # TAREFAS SELECIONADAS
    # ========================================================

    def obter_tarefas_selecionadas(self):

        selecionadas = []

        for indice in range(
            self.tasks.count()
        ):

            item = self.tasks.item(
                indice
            )

            if (
                item.checkState()
                == Qt.CheckState.Checked
            ):

                selecionadas.append(
                    item.data(
                        Qt.ItemDataRole.UserRole
                    )
                )

        return selecionadas

    # ========================================================
    # EXECUTAR SELECIONADAS
    # ========================================================

    def executar_selecionadas(self):

        empresa_id = (
            self.empresa_selecionada_id()
        )

        estabelecimento_id = (
            self.estabelecimento_selecionado_id()
        )

        if empresa_id is None:

            QMessageBox.warning(
                self,
                "Empresa",
                "Selecione uma empresa.",
            )

            return

        if estabelecimento_id is None:

            QMessageBox.warning(
                self,
                "Estabelecimento",
                "Selecione um estabelecimento.",
            )

            return

        tarefas = (
            self.obter_tarefas_selecionadas()
        )

        if not tarefas:

            QMessageBox.warning(
                self,
                "Tarefas",
                (
                    "Selecione pelo menos "
                    "uma tarefa."
                ),
            )

            return

        try:

            competencia = (
                self.obter_competencia_atual(
                    criar=True
                )
            )

            if competencia is None:

                raise RuntimeError(
                    (
                        "Não foi possível criar "
                        "ou localizar a competência."
                    )
                )

            self.execucoes_atuais = []

            for tarefa in tarefas:

                execucao = (
                    self.execution_service
                    .obter_ou_criar_execucao(
                        competencia_id=competencia.id,
                        task_key=tarefa["key"],
                        task_name=tarefa["name"],
                    )
                )

                self.execution_service.salvar_checkpoint(
                    execution_id=execucao.id,
                    step_key="aguardando_treinamento",
                    item_key=None,
                    payload={
                        "empresa_id": empresa_id,
                        "estabelecimento_id": (
                            estabelecimento_id
                        ),
                        "competencia_id": competencia.id,
                        "mes": competencia.mes,
                        "ano": competencia.ano,
                        "task_key": tarefa["key"],
                        "task_name": tarefa["name"],
                    },
                )

                self.execution_service.alterar_status(
                    execution_id=execucao.id,
                    status="AGUARDANDO_TREINAMENTO",
                )

                self.execucoes_atuais.append(
                    execucao.id
                )

            self.atualizar_status_tarefas()

            QMessageBox.information(
                self,
                "Preparado",
                (
                    "Competência preparada.\n"
                    "Execuções registradas.\n"
                    "Checkpoints criados."
                ),
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    # ========================================================
    # PAUSAR
    # ========================================================

    def pausar_execucoes(self):

        if not self.execucoes_atuais:

            QMessageBox.warning(
                self,
                "Pausar",
                "Não existe execução atual.",
            )

            return

        try:

            for execution_id in self.execucoes_atuais:

                self.execution_service.pausar(
                    execution_id
                )

            self.atualizar_status_tarefas()

            self.label_status.setText(
                "Status: PAUSADO"
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    # ========================================================
    # CONTINUAR
    # ========================================================

    def continuar_execucoes(self):

        if not self.execucoes_atuais:

            QMessageBox.warning(
                self,
                "Continuar",
                "Não existe execução atual.",
            )

            return

        try:

            for execution_id in self.execucoes_atuais:

                contexto = (
                    self.execution_service
                    .obter_contexto_retomada(
                        execution_id
                    )
                )

                if (
                    contexto["step_key"]
                    == "aguardando_treinamento"
                ):

                    status = (
                        "AGUARDANDO_TREINAMENTO"
                    )

                else:

                    status = (
                        "EM_EXECUCAO"
                    )

                self.execution_service.alterar_status(
                    execution_id=execution_id,
                    status=status,
                )

            self.atualizar_status_tarefas()

            self.label_status.setText(
                "Status: execução retomada."
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    # ========================================================
    # PARAR
    # ========================================================

    def parar_execucoes(self):

        if not self.execucoes_atuais:

            QMessageBox.warning(
                self,
                "Parar",
                "Não existe execução atual.",
            )

            return

        resposta = QMessageBox.question(
            self,
            "Parar robô",
            (
                "Deseja interromper a execução?\n\n"
                "O checkpoint será preservado."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
        )

        if (
            resposta
            != QMessageBox.StandardButton.Yes
        ):

            return

        try:

            for execution_id in self.execucoes_atuais:

                self.execution_service.aguardar_intervencao(
                    execution_id=execution_id,
                    motivo=(
                        "Interrompido manualmente."
                    ),
                )

            self.execucoes_atuais = []

            self.atualizar_status_tarefas()

            self.label_status.setText(
                (
                    "Status: INTERROMPIDO. "
                    "Checkpoint preservado."
                )
            )

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro),
            )

    # ========================================================
    # EMPRESAS
    # ========================================================

    def abrir_empresas(self):

        if self.empresa_form is None:

            self.empresa_form = (
                EmpresaForm()
            )

            self.empresa_form.empresa_salva.connect(
                self.carregar_empresas
            )

        self.empresa_form.show()
        self.empresa_form.raise_()
        self.empresa_form.activateWindow()

    # ========================================================
    # ESTABELECIMENTOS
    # ========================================================

    def abrir_filiais(self):

        if self.filial_form is None:

            self.filial_form = (
                FilialForm()
            )

            self.filial_form.filial_salva.connect(
                self.carregar_estabelecimentos
            )

        self.filial_form.carregar_empresas()

        self.filial_form.show()
        self.filial_form.raise_()
        self.filial_form.activateWindow()

    # ========================================================
    # IE
    # ========================================================

    def abrir_inscricoes_estaduais(self):

        if self.ie_form is None:

            self.ie_form = (
                InscricaoEstadualForm()
            )

        self.ie_form.carregar_empresas()

        self.ie_form.show()
        self.ie_form.raise_()
        self.ie_form.activateWindow()

    # ========================================================
    # IM
    # ========================================================

    def abrir_inscricoes_municipais(self):

        if self.im_form is None:

            self.im_form = (
                InscricaoMunicipalForm()
            )

        self.im_form.carregar_empresas()

        self.im_form.show()
        self.im_form.raise_()
        self.im_form.activateWindow()

    # ========================================================
    # CREDENCIAIS
    # ========================================================

    def abrir_credenciais(self):

        if self.credencial_form is None:

            self.credencial_form = (
                CredencialForm()
            )

        self.credencial_form.carregar_empresas()
        self.credencial_form.carregar_lista()

        self.credencial_form.show()
        self.credencial_form.raise_()
        self.credencial_form.activateWindow()

    # ========================================================
    # HISTÓRICO
    # ========================================================

    def abrir_historico(self):

        if self.historico_form is None:

            self.historico_form = (
                HistoricoForm()
            )

        self.historico_form.carregar_empresas()

        self.historico_form.show()
        self.historico_form.raise_()
        self.historico_form.activateWindow()
