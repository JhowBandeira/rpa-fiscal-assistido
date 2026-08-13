import calendar

from playwright.sync_api import (
    Page,
    Locator,
)

from rpa.totvs_navigation import (
    TotvsNavigation,
)


class SftNavigation:

    def __init__(
        self,
        page: Page,
    ):
        self.page = page
        self.base = TotvsNavigation(page)

    # ========================================================
    # CONTEXTOS
    # ========================================================

    def _contextos(self):

        yield self.page

        for frame in self.page.frames:

            if frame == self.page.main_frame:
                continue

            yield frame

    # ========================================================
    # DATAS DA COMPETÊNCIA
    # ========================================================

    def calcular_periodo(
        self,
        mes: int,
        ano: int,
    ):

        ultimo_dia = calendar.monthrange(
            ano,
            mes,
        )[1]

        data_inicial = (
            f"01/{mes:02d}/{ano:04d}"
        )

        data_final = (
            f"{ultimo_dia:02d}/"
            f"{mes:02d}/"
            f"{ano:04d}"
        )

        return (
            data_inicial,
            data_final,
        )

    # ========================================================
    # SOMENTE NÚMEROS
    # ========================================================

    def _somente_numeros(
        self,
        valor,
    ) -> str:

        if valor is None:
            return ""

        return "".join(
            caractere
            for caractere in str(valor)
            if caractere.isdigit()
        )

    # ========================================================
    # DIGITAÇÃO HUMANA
    # ========================================================

    def digitar_humano(
        self,
        campo: Locator,
        valor: str,
    ):

        campo.click()

        self.page.wait_for_timeout(
            250
        )

        campo.press(
            "Control+A"
        )

        self.page.wait_for_timeout(
            150
        )

        campo.press(
            "Backspace"
        )

        self.page.wait_for_timeout(
            150
        )

        campo.press_sequentially(
            valor,
            delay=90,
        )

        self.page.wait_for_timeout(
            300
        )

    # ========================================================
    # ABRIR CONSULTAS
    # ========================================================

    def abrir_consultas(
        self,
    ):

        self.base.aguardar_texto(
            "Consultas",
            timeout_ms=30000,
        )

        item = self.base.localizar_texto(
            "Consultas",
            exact=False,
        )

        item.click()

        self.page.wait_for_timeout(
            700
        )

    # ========================================================
    # ABRIR CADASTROS
    # ========================================================

    def abrir_cadastros(
        self,
    ):

        self.base.aguardar_texto(
            "Cadastros",
            timeout_ms=15000,
        )

        item = self.base.localizar_texto(
            "Cadastros",
            exact=False,
        )

        item.click()

        self.page.wait_for_timeout(
            700
        )

    # ========================================================
    # ABRIR GENÉRICOS
    # ========================================================

    def abrir_genericos(
        self,
    ):

        possibilidades = [
            "Genericos",
            "Genéricos",
        ]

        ultimo_erro = None

        for texto in possibilidades:

            try:

                item = self.base.localizar_texto(
                    texto,
                    exact=False,
                )

                item.click()

                self.page.wait_for_timeout(
                    1200
                )

                return

            except Exception as erro:

                ultimo_erro = erro

        raise RuntimeError(
            (
                "Não foi possível abrir Genéricos. "
                f"Detalhe: {ultimo_erro}"
            )
        )

    # ========================================================
    # LOCALIZAR PESQUISA DO SFT
    # ========================================================

    def localizar_pesquisa_sft(
        self,
    ) -> Locator:

        for contexto in self._contextos():

            try:

                campos = contexto.locator(
                    "wa-text-input input:visible"
                )

                for indice in range(
                    campos.count()
                ):

                    campo = campos.nth(
                        indice
                    )

                    try:

                        if not campo.is_visible():
                            continue

                        caixa = campo.bounding_box()

                        if caixa is None:
                            continue

                        if caixa["width"] < 40:
                            continue

                        return campo

                    except Exception:
                        continue

            except Exception:
                continue

        for contexto in self._contextos():

            try:

                titulos = contexto.get_by_text(
                    "Selecione o Arquivo",
                    exact=False,
                )

                for indice_titulo in range(
                    titulos.count()
                ):

                    titulo = titulos.nth(
                        indice_titulo
                    )

                    if not titulo.is_visible():
                        continue

                    caixa_titulo = (
                        titulo.bounding_box()
                    )

                    if caixa_titulo is None:
                        continue

                    inputs = contexto.locator(
                        'input[type="text"]:visible'
                    )

                    melhor = None
                    melhor_distancia = None

                    for indice_input in range(
                        inputs.count()
                    ):

                        campo = inputs.nth(
                            indice_input
                        )

                        caixa = campo.bounding_box()

                        if caixa is None:
                            continue

                        if (
                            caixa["y"]
                            <= caixa_titulo["y"]
                        ):
                            continue

                        distancia = (
                            abs(
                                caixa["x"]
                                - caixa_titulo["x"]
                            )
                            + abs(
                                caixa["y"]
                                - caixa_titulo["y"]
                            )
                        )

                        if (
                            melhor_distancia is None
                            or distancia
                            < melhor_distancia
                        ):

                            melhor = campo
                            melhor_distancia = distancia

                    if melhor is not None:
                        return melhor

            except Exception:
                continue

        raise RuntimeError(
            (
                "A janela 'Selecione o Arquivo' foi aberta, "
                "mas o campo de pesquisa não foi localizado."
            )
        )

    # ========================================================
    # PESQUISAR SFT
    #
    # DIGITA SFT E CLICA EM OK.
    # NÃO PRECISA CLICAR NA LINHA.
    # ========================================================

    def pesquisar_sft(
        self,
    ):

        self.base.aguardar_texto(
            "Selecione o Arquivo",
            timeout_ms=20000,
        )

        self.page.wait_for_timeout(
            700
        )

        campo = (
            self.localizar_pesquisa_sft()
        )

        self.digitar_humano(
            campo,
            "SFT",
        )

        self.page.wait_for_timeout(
            600
        )

        botao_ok = (
            self.base.localizar_botao(
                "Ok"
            )
        )

        botao_ok.click()

        self.page.wait_for_timeout(
            2500
        )

        textos_confirmacao = [
            "Livro Fiscal Por Item de Nf",
            "Livro Fiscal por Item de NF",
            "Consulta Genérica - Livro Fiscal",
            "SFT - Livro Fiscal",
        ]

        aberto = False

        for _ in range(30):

            for texto in textos_confirmacao:

                try:

                    self.base.localizar_texto(
                        texto,
                        exact=False,
                    )

                    aberto = True
                    break

                except Exception:
                    continue

            if aberto:
                break

            self.page.wait_for_timeout(
                500
            )

        if not aberto:

            raise RuntimeError(
                (
                    "O robô digitou SFT e clicou em OK, "
                    "mas a consulta SFT não abriu "
                    "dentro do tempo esperado."
                )
            )

        self.page.wait_for_timeout(
            1000
        )

    # ========================================================
    # ABRIR FILTRO
    #
    # FLUXO CORRETO:
    #
    # SFT
    # → FILTRAR
    # → GERENCIADOR DE FILTROS
    # → CRIAR FILTRO
    # → JANELA CRIAR FILTRO
    # ========================================================

    def abrir_filtro(
        self,
    ):

        # ====================================================
        # CLICA EM FILTRAR
        # ====================================================

        self.base.aguardar_texto(
            "Filtrar",
            timeout_ms=30000,
        )

        item = self.base.localizar_texto(
            "Filtrar",
            exact=True,
        )

        item.click()

        self.page.wait_for_timeout(
            1000
        )

        # ====================================================
        # AGUARDA GERENCIADOR DE FILTROS
        # ====================================================

        self.base.aguardar_texto(
            "Gerenciador de Filtros",
            timeout_ms=15000,
        )

        self.page.wait_for_timeout(
            500
        )

        # ====================================================
        # AGORA CLICA EM CRIAR FILTRO
        # ====================================================

        botao_criar = (
            self.base.localizar_botao(
                "Criar Filtro"
            )
        )

        botao_criar.click()

        self.page.wait_for_timeout(
            800
        )

        # ====================================================
        # CONFIRMA QUE A JANELA DE CRIAÇÃO ABRIU
        # ====================================================

        self.base.aguardar_texto(
            "Nome do Filtro",
            timeout_ms=15000,
        )

        self.base.aguardar_texto(
            "Campo",
            timeout_ms=15000,
        )

        self.base.aguardar_texto(
            "Operador",
            timeout_ms=15000,
        )

        self.base.aguardar_texto(
            "Expressão",
            timeout_ms=15000,
        )

        self.page.wait_for_timeout(
            500
        )

    # ========================================================
    # SELECT / COMBO
    # ========================================================

    def _selecionar_opcao_dropdown(
        self,
        rotulo: str,
        valor: str,
    ):

        # ====================================================
        # TENTA SELECT NATIVO
        # ====================================================

        for contexto in self._contextos():

            try:

                selects = contexto.locator(
                    "select:visible"
                )

                for indice in range(
                    selects.count()
                ):

                    select = selects.nth(
                        indice
                    )

                    opcoes = select.locator(
                        "option"
                    )

                    for idx in range(
                        opcoes.count()
                    ):

                        texto_opcao = (
                            opcoes.nth(
                                idx
                            )
                            .inner_text()
                            .strip()
                        )

                        if texto_opcao == valor:

                            select.select_option(
                                label=valor
                            )

                            return

            except Exception:
                continue

        # ====================================================
        # COMPONENTE CUSTOMIZADO
        # ====================================================

        for contexto in self._contextos():

            try:

                rotulos = contexto.get_by_text(
                    rotulo,
                    exact=True,
                )

                for indice in range(
                    rotulos.count()
                ):

                    elemento = rotulos.nth(
                        indice
                    )

                    try:

                        if not elemento.is_visible():
                            continue

                    except Exception:
                        continue

                    container = elemento

                    for _ in range(6):

                        try:

                            container = (
                                container.locator(
                                    "xpath=.."
                                )
                            )

                            combos = (
                                container.locator(
                                    (
                                        "[role='combobox']:visible, "
                                        "select:visible, "
                                        "input:visible"
                                    )
                                )
                            )

                            if combos.count() == 0:
                                continue

                            combo = combos.first

                            combo.click()

                            self.page.wait_for_timeout(
                                250
                            )

                            opcao = (
                                self.base.localizar_texto(
                                    valor,
                                    exact=True,
                                )
                            )

                            opcao.click()

                            self.page.wait_for_timeout(
                                250
                            )

                            return

                        except Exception:
                            continue

            except Exception:
                continue

        raise RuntimeError(
            (
                f"Não foi possível selecionar "
                f"'{valor}' no campo '{rotulo}'."
            )
        )

    # ========================================================
    # CAMPO
    # ========================================================

    def _selecionar_campo(
        self,
        valor: str,
    ):

        self._selecionar_opcao_dropdown(
            rotulo="Campo",
            valor=valor,
        )

    # ========================================================
    # OPERADOR
    # ========================================================

    def _selecionar_operador(
        self,
        valor: str,
    ):

        self._selecionar_opcao_dropdown(
            rotulo="Operador",
            valor=valor,
        )

    # ========================================================
    # LOCALIZAR INPUT DA EXPRESSÃO
    #
    # DATA ENTRADA FICA EM SHADOW DOM OPEN
    # ========================================================

    def localizar_input_expressao(
        self,
    ) -> Locator:

        for contexto in self._contextos():

            try:

                rotulos = contexto.get_by_text(
                    "Expressão",
                    exact=True,
                )

            except Exception:
                continue

            for indice_rotulo in range(
                rotulos.count()
            ):

                rotulo = rotulos.nth(
                    indice_rotulo
                )

                try:

                    if not rotulo.is_visible():
                        continue

                    caixa_rotulo = (
                        rotulo.bounding_box()
                    )

                    if caixa_rotulo is None:
                        continue

                except Exception:
                    continue

                inputs = contexto.locator(
                    "input:visible"
                )

                melhor_input = None
                melhor_distancia = None

                centro_rotulo_x = (
                    caixa_rotulo["x"]
                    + caixa_rotulo["width"] / 2
                )

                centro_rotulo_y = (
                    caixa_rotulo["y"]
                    + caixa_rotulo["height"] / 2
                )

                for indice_input in range(
                    inputs.count()
                ):

                    campo = inputs.nth(
                        indice_input
                    )

                    try:

                        caixa = campo.bounding_box()

                        if caixa is None:
                            continue

                    except Exception:
                        continue

                    centro_input_x = (
                        caixa["x"]
                        + caixa["width"] / 2
                    )

                    centro_input_y = (
                        caixa["y"]
                        + caixa["height"] / 2
                    )

                    dx = (
                        centro_input_x
                        - centro_rotulo_x
                    )

                    dy = abs(
                        centro_input_y
                        - centro_rotulo_y
                    )

                    if dx < -40:
                        continue

                    if dx > 600:
                        continue

                    if dy > 80:
                        continue

                    distancia = (
                        abs(dx)
                        + dy
                    )

                    if (
                        melhor_distancia is None
                        or distancia
                        < melhor_distancia
                    ):

                        melhor_distancia = distancia
                        melhor_input = campo

                if melhor_input is not None:
                    return melhor_input

        raise RuntimeError(
            (
                "Não foi possível localizar o campo "
                "Expressão/Data Entrada dentro "
                "do Shadow DOM."
            )
        )

    # ========================================================
    # PREENCHER EXPRESSÃO
    # ========================================================

    def _preencher_expressao(
        self,
        valor: str,
    ):

        campo = (
            self.localizar_input_expressao()
        )

        self.digitar_humano(
            campo,
            valor,
        )

        campo.press(
            "Tab"
        )

        self.page.wait_for_timeout(
            400
        )

        try:

            valor_atual = (
                campo.input_value()
            )

        except Exception:

            valor_atual = ""

        if (
            self._somente_numeros(
                valor_atual
            )
            != self._somente_numeros(
                valor
            )
        ):

            raise RuntimeError(
                (
                    "A data do filtro SFT não ficou "
                    "com o valor esperado.\n\n"
                    f"Esperado: {valor}\n"
                    f"Encontrado: {valor_atual}"
                )
            )

    # ========================================================
    # BOTÃO
    # ========================================================

    def _clicar_botao(
        self,
        texto: str,
    ):

        botao = (
            self.base.localizar_botao(
                texto
            )
        )

        botao.click()

        self.page.wait_for_timeout(
            300
        )

    # ========================================================
    # TEXTO EXATO
    # ========================================================

    def _clicar_texto_exato(
        self,
        texto: str,
    ):

        item = (
            self.base.localizar_texto(
                texto,
                exact=True,
            )
        )

        item.click()

        self.page.wait_for_timeout(
            250
        )

    # ========================================================
    # CRIAR FILTRO DA COMPETÊNCIA
    # ========================================================

    def criar_filtro_competencia(
        self,
        mes: int,
        ano: int,
    ):

        (
            data_inicial,
            data_final,
        ) = self.calcular_periodo(
            mes,
            ano,
        )

        # ====================================================
        # PRIMEIRA CONDIÇÃO
        #
        # DATA ENTRADA >= PRIMEIRO DIA
        # ====================================================

        self._selecionar_campo(
            "Data Entrada"
        )

        self._selecionar_operador(
            "Maior ou igual a"
        )

        self._preencher_expressao(
            data_inicial
        )

        self._clicar_botao(
            "Adicionar"
        )

        self.page.wait_for_timeout(
            500
        )

        # ====================================================
        # E
        # ====================================================

        self._clicar_texto_exato(
            "e"
        )

        self.page.wait_for_timeout(
            400
        )

        # ====================================================
        # SEGUNDA CONDIÇÃO
        #
        # DATA ENTRADA <= ÚLTIMO DIA
        # ====================================================

        self._selecionar_campo(
            "Data Entrada"
        )

        self._selecionar_operador(
            "Menor ou igual a"
        )

        self._preencher_expressao(
            data_final
        )

        self._clicar_botao(
            "Adicionar"
        )

        self.page.wait_for_timeout(
            500
        )

        # ====================================================
        # SALVAR
        # ====================================================

        self._clicar_botao(
            "Salvar"
        )

        self.page.wait_for_timeout(
            1000
        )

        return (
            data_inicial,
            data_final,
        )

    # ========================================================
    # CHECKBOX MARCADO?
    # ========================================================

    def _checkbox_marcado(
        self,
        check: Locator,
    ) -> bool:

        try:

            return check.is_checked()

        except Exception:
            pass

        try:

            return (
                check.get_attribute(
                    "aria-checked"
                )
                == "true"
            )

        except Exception:
            return False

    # ========================================================
    # CHECKBOX ASSOCIADO A TEXTO
    # ========================================================

    def _checkbox_proximo_texto(
        self,
        texto: str,
    ) -> Locator:

        for contexto in self._contextos():

            try:

                textos = contexto.get_by_text(
                    texto,
                    exact=False,
                )

                for indice in range(
                    textos.count()
                ):

                    item = textos.nth(
                        indice
                    )

                    try:

                        if not item.is_visible():
                            continue

                    except Exception:
                        continue

                    container = item

                    for _ in range(7):

                        try:

                            container = (
                                container.locator(
                                    "xpath=.."
                                )
                            )

                            checks = (
                                container.locator(
                                    (
                                        'input[type="checkbox"], '
                                        '[role="checkbox"]'
                                    )
                                )
                            )

                            if checks.count() > 0:
                                return checks.first

                        except Exception:
                            continue

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                f"o checkbox associado a '{texto}'."
            )
        )

    # ========================================================
    # CONFIGURAR FILTRO CRIADO
    # ========================================================

    def configurar_filtro_criado(
        self,
    ):

        self.base.aguardar_texto(
            "Gerenciador de Filtros",
            timeout_ms=15000,
        )

        # ====================================================
        # DESMARCA FILTRAR FILIAL PADRÃO
        # ====================================================

        try:

            check_padrao = (
                self._checkbox_proximo_texto(
                    "Filtrar Filial Padrão"
                )
            )

            if self._checkbox_marcado(
                check_padrao
            ):

                check_padrao.click()

        except Exception:
            pass

        # ====================================================
        # MARCA FILTRO DA COMPETÊNCIA
        # ====================================================

        check_data = (
            self._checkbox_proximo_texto(
                "Data Entrada Maior ou igual"
            )
        )

        if not self._checkbox_marcado(
            check_data
        ):

            check_data.click()

        # ====================================================
        # APLICA FILTRO
        # ====================================================

        self._clicar_botao(
            "Aplicar filtros selecionados"
        )

        self.page.wait_for_timeout(
            5000
        )

    # ========================================================
    # ABRIR DICIONÁRIO
    # ========================================================

    def abrir_dicionario(
        self,
    ):

        self._clicar_botao(
            "Dicionário"
        )

        self.page.wait_for_timeout(
            800
        )

    # ========================================================
    # MARCAR TODOS NO DICIONÁRIO
    # ========================================================

    def marcar_todos_dicionario(
        self,
    ):

        self.base.aguardar_texto(
            "Campos exibidos",
            timeout_ms=15000,
        )

        # ====================================================
        # DESMARCA "SENDO USADO SOMENTE NO BROWSE"
        # ====================================================

        try:

            check_browse = (
                self._checkbox_proximo_texto(
                    "Sendo usado somente"
                )
            )

            if self._checkbox_marcado(
                check_browse
            ):

                check_browse.click()

        except Exception:
            pass

        # ====================================================
        # MARCA TODOS
        # ====================================================

        for contexto in self._contextos():

            try:

                checks = contexto.locator(
                    (
                        'input[type="checkbox"]:visible, '
                        '[role="checkbox"]:visible'
                    )
                )

                for indice in range(
                    checks.count()
                ):

                    check = checks.nth(
                        indice
                    )

                    try:

                        if not check.is_enabled():
                            continue

                        if not self._checkbox_marcado(
                            check
                        ):

                            check.click()

                    except Exception:
                        continue

            except Exception:
                continue

        self._clicar_botao(
            "Ok"
        )

        self.page.wait_for_timeout(
            900
        )

    # ========================================================
    # EXPORTAÇÃO
    # ========================================================

    def exportar_csv_xml_excel(
        self,
    ):

        self._clicar_botao(
            "Exp. CSV"
        )

        self.page.wait_for_timeout(
            800
        )

        self.base.aguardar_texto(
            "Formato",
            timeout_ms=15000,
        )

        # ====================================================
        # FORMATO XML
        # ====================================================

        self._selecionar_opcao_dropdown(
            rotulo="Formato",
            valor="XML",
        )

        # ====================================================
        # MANTÉM MICROSOFT EXCEL
        # ====================================================

        for contexto in self._contextos():

            try:

                textos = contexto.get_by_text(
                    "Microsoft Excel",
                    exact=False,
                )

                for indice in range(
                    textos.count()
                ):

                    texto = textos.nth(
                        indice
                    )

                    try:

                        if not texto.is_visible():
                            continue

                    except Exception:
                        continue

                    container = texto

                    for _ in range(5):

                        try:

                            container = (
                                container.locator(
                                    "xpath=.."
                                )
                            )

                            radios = (
                                container.locator(
                                    (
                                        'input[type="radio"], '
                                        '[role="radio"]'
                                    )
                                )
                            )

                            if radios.count() == 0:
                                continue

                            radio = radios.first

                            try:

                                marcado = (
                                    radio.is_checked()
                                )

                            except Exception:

                                marcado = (
                                    radio.get_attribute(
                                        "aria-checked"
                                    )
                                    == "true"
                                )

                            if not marcado:
                                radio.click()

                            break

                        except Exception:
                            continue

            except Exception:
                continue

        # ====================================================
        # CONFIRMAR EXPORTAÇÃO
        # ====================================================

        self._clicar_botao(
            "Confirmar"
        )

        self.page.wait_for_timeout(
            2500
        )
