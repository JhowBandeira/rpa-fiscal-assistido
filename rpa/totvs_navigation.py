from playwright.sync_api import (
    Page,
    Locator,
)


class TotvsNavigation:

    def __init__(
        self,
        page: Page,
    ):

        self.page = page

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
    # LOCALIZAR TEXTO
    # ========================================================

    def localizar_texto(
        self,
        texto: str,
        exact: bool = False,
    ) -> Locator:

        for contexto in self._contextos():

            try:

                locator = contexto.get_by_text(
                    texto,
                    exact=exact,
                )

                for indice in range(
                    locator.count()
                ):

                    item = locator.nth(
                        indice
                    )

                    try:

                        if item.is_visible():
                            return item

                    except Exception:
                        continue

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                f"o texto: {texto}"
            )
        )

    # ========================================================
    # LOCALIZAR BOTÃO
    # ========================================================

    def localizar_botao(
        self,
        texto: str,
    ) -> Locator:

        for contexto in self._contextos():

            candidatos = [
                contexto.get_by_role(
                    "button",
                    name=texto,
                    exact=True,
                ),
                contexto.locator(
                    f'button:has-text("{texto}")'
                ),
                contexto.get_by_text(
                    texto,
                    exact=True,
                ),
            ]

            for candidato in candidatos:

                try:

                    for indice in range(
                        candidato.count()
                    ):

                        item = candidato.nth(
                            indice
                        )

                        if item.is_visible():
                            return item

                except Exception:
                    continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                f"o botão: {texto}"
            )
        )

    # ========================================================
    # AGUARDAR TEXTO
    # ========================================================

    def aguardar_texto(
        self,
        texto: str,
        timeout_ms: int = 30000,
    ):

        tempo = 0
        intervalo = 500

        while tempo < timeout_ms:

            try:

                self.localizar_texto(
                    texto,
                    exact=False,
                )

                return

            except Exception:
                pass

            self.page.wait_for_timeout(
                intervalo
            )

            tempo += intervalo

        raise RuntimeError(
            (
                f"O texto '{texto}' não apareceu "
                "dentro do tempo esperado."
            )
        )

    # ========================================================
    # CLICAR LUPA PELO NOME DO CAMPO
    # ========================================================

    def clicar_lupa_campo(
        self,
        nome_campo: str,
    ):

        for contexto in self._contextos():

            try:

                textos = contexto.get_by_text(
                    nome_campo,
                    exact=True,
                )

                for indice in range(
                    textos.count()
                ):

                    rotulo = textos.nth(
                        indice
                    )

                    try:

                        if not rotulo.is_visible():
                            continue

                    except Exception:
                        continue

                    container = rotulo

                    for _ in range(7):

                        try:

                            container = (
                                container.locator(
                                    "xpath=.."
                                )
                            )

                            inputs = (
                                container.locator(
                                    "input:visible"
                                )
                            )

                            botoes = (
                                container.locator(
                                    (
                                        "button:visible, "
                                        "[role='button']:visible"
                                    )
                                )
                            )

                            if (
                                inputs.count() > 0
                                and botoes.count() > 0
                            ):

                                campo = inputs.first

                                caixa_campo = (
                                    campo.bounding_box()
                                )

                                if caixa_campo is None:
                                    continue

                                melhor_botao = None
                                melhor_distancia = None

                                for indice_botao in range(
                                    botoes.count()
                                ):

                                    botao = botoes.nth(
                                        indice_botao
                                    )

                                    try:

                                        caixa_botao = (
                                            botao.bounding_box()
                                        )

                                        if caixa_botao is None:
                                            continue

                                        centro_campo_x = (
                                            caixa_campo["x"]
                                            + (
                                                caixa_campo["width"]
                                                / 2
                                            )
                                        )

                                        centro_campo_y = (
                                            caixa_campo["y"]
                                            + (
                                                caixa_campo["height"]
                                                / 2
                                            )
                                        )

                                        centro_botao_x = (
                                            caixa_botao["x"]
                                            + (
                                                caixa_botao["width"]
                                                / 2
                                            )
                                        )

                                        centro_botao_y = (
                                            caixa_botao["y"]
                                            + (
                                                caixa_botao["height"]
                                                / 2
                                            )
                                        )

                                        distancia = (
                                            abs(
                                                centro_botao_x
                                                - centro_campo_x
                                            )
                                            + abs(
                                                centro_botao_y
                                                - centro_campo_y
                                            )
                                        )

                                        if (
                                            melhor_distancia is None
                                            or distancia
                                            < melhor_distancia
                                        ):

                                            melhor_distancia = (
                                                distancia
                                            )

                                            melhor_botao = (
                                                botao
                                            )

                                    except Exception:
                                        continue

                                if melhor_botao is not None:

                                    melhor_botao.click()

                                    self.page.wait_for_timeout(
                                        800
                                    )

                                    return

                        except Exception:
                            continue

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar a lupa "
                f"do campo '{nome_campo}'."
            )
        )

    # ========================================================
    # RADIO SELECIONADO?
    # ========================================================

    def _radio_esta_selecionado(
        self,
        radio: Locator,
    ) -> bool:

        try:

            if radio.is_checked():
                return True

        except Exception:
            pass

        try:

            aria_checked = (
                radio.get_attribute(
                    "aria-checked"
                )
            )

            if (
                aria_checked is not None
                and aria_checked.lower() == "true"
            ):

                return True

        except Exception:
            pass

        try:

            classe = (
                radio.get_attribute(
                    "class"
                )
                or ""
            ).lower()

            for indicador in [
                "selected",
                "checked",
                "active",
            ]:

                if indicador in classe:
                    return True

        except Exception:
            pass

        return False

    # ========================================================
    # LOCALIZAR LINHA POR TEXTO
    # ========================================================

    def _localizar_linha_por_texto(
        self,
        texto: str,
    ) -> Locator:

        self.aguardar_texto(
            texto,
            timeout_ms=20000,
        )

        for contexto in self._contextos():

            try:

                elementos = (
                    contexto.get_by_text(
                        texto,
                        exact=True,
                    )
                )

                for indice in range(
                    elementos.count()
                ):

                    elemento = (
                        elementos.nth(
                            indice
                        )
                    )

                    try:

                        if not elemento.is_visible():
                            continue

                    except Exception:
                        continue

                    # ==========================================
                    # TABELA HTML
                    # ==========================================

                    try:

                        linha = (
                            elemento.locator(
                                "xpath=ancestor::tr[1]"
                            )
                        )

                        if (
                            linha.count() > 0
                            and linha.is_visible()
                        ):

                            return linha

                    except Exception:
                        pass

                    # ==========================================
                    # FALLBACK
                    # ==========================================

                    atual = elemento

                    for _ in range(8):

                        try:

                            atual = atual.locator(
                                "xpath=.."
                            )

                            radios = atual.locator(
                                (
                                    "input[type='radio'], "
                                    "[role='radio']"
                                )
                            )

                            if radios.count() > 0:
                                return atual

                        except Exception:
                            break

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                f"a linha de '{texto}'."
            )
        )

    # ========================================================
    # CLICAR SELECIONAR
    # ========================================================

    def clicar_selecionar(
        self,
    ):

        botao = (
            self.localizar_botao(
                "Selecionar"
            )
        )

        botao.click()

        self.page.wait_for_timeout(
            1200
        )

    # ========================================================
    # FILIAL PELO CNPJ
    # ========================================================

    def selecionar_filial_por_cnpj(
        self,
        cnpj: str,
    ):

        cnpj_limpo = (
            cnpj.replace(".", "")
            .replace("/", "")
            .replace("-", "")
            .strip()
        )

        linha = (
            self._localizar_linha_por_texto(
                cnpj_limpo
            )
        )

        radios = linha.locator(
            (
                "input[type='radio'], "
                "[role='radio']"
            )
        )

        if radios.count() == 0:

            raise RuntimeError(
                (
                    "A filial foi localizada pelo CNPJ, "
                    "mas o seletor da linha "
                    "não foi encontrado."
                )
            )

        radio = radios.first

        if not self._radio_esta_selecionado(
            radio
        ):

            radio.click()

            self.page.wait_for_timeout(
                400
            )

        self.clicar_selecionar()

    # ========================================================
    # AMBIENTE 9 - LIVROS FISCAIS
    # ========================================================

    def selecionar_ambiente_livros_fiscais(
        self,
    ):

        linha = (
            self._localizar_linha_por_texto(
                "Livros Fiscais"
            )
        )

        try:

            texto_linha = linha.inner_text()

        except Exception:

            texto_linha = ""

        if (
            "Livros Fiscais"
            not in texto_linha
        ):

            raise RuntimeError(
                (
                    "A linha localizada não corresponde "
                    "ao ambiente Livros Fiscais."
                )
            )

        radios = linha.locator(
            (
                "input[type='radio'], "
                "[role='radio']"
            )
        )

        if radios.count() == 0:

            raise RuntimeError(
                (
                    "O ambiente Livros Fiscais foi "
                    "localizado, mas o seletor da linha "
                    "não foi encontrado."
                )
            )

        radio = radios.first

        if not self._radio_esta_selecionado(
            radio
        ):

            radio.click()

            self.page.wait_for_timeout(
                400
            )

        self.clicar_selecionar()

    # ========================================================
    # ENTRAR
    # ========================================================

    def entrar_no_ambiente(
        self,
    ):

        botao = (
            self.localizar_botao(
                "Entrar"
            )
        )

        botao.click()

        self.page.wait_for_timeout(
            5000
        )

    # ========================================================
    # MISCELÂNEA
    # ========================================================

    def abrir_miscelanea(
        self,
    ):

        ultimo_erro = None

        for texto in [
            "Miscelanea",
            "Miscelânea",
        ]:

            try:

                item = (
                    self.localizar_texto(
                        texto,
                        exact=False,
                    )
                )

                item.click()

                self.page.wait_for_timeout(
                    1000
                )

                return

            except Exception as erro:

                ultimo_erro = erro

        raise RuntimeError(
            (
                "Não foi possível abrir Miscelânea. "
                f"Detalhe: {ultimo_erro}"
            )
        )

    # ========================================================
    # ACERTOS
    # ========================================================

    def abrir_acertos(
        self,
    ):

        self.aguardar_texto(
            "Acertos",
            timeout_ms=15000,
        )

        item = (
            self.localizar_texto(
                "Acertos",
                exact=False,
            )
        )

        item.click()

        self.page.wait_for_timeout(
            1000
        )

    # ========================================================
    # DATA FECH/TO FISCAL
    # ========================================================

    def abrir_data_fechamento_fiscal(
        self,
    ):

        ultimo_erro = None

        for texto in [
            "Data Fech/to Fiscal",
            "Data Fech",
        ]:

            try:

                item = (
                    self.localizar_texto(
                        texto,
                        exact=False,
                    )
                )

                item.click()

                self.page.wait_for_timeout(
                    2500
                )

                return

            except Exception as erro:

                ultimo_erro = erro

        raise RuntimeError(
            (
                "Não foi possível abrir "
                "'Data Fech/to Fiscal'. "
                f"Detalhe: {ultimo_erro}"
            )
        )

    # ========================================================
    # CONFIRMAR TELA
    # ========================================================

    def confirmar_tela_fechamento(
        self,
    ):

        for texto in [
            "Alteração na data limite",
            "MV_DATAFIS",
            "Nova data",
        ]:

            try:

                self.aguardar_texto(
                    texto,
                    timeout_ms=10000,
                )

                return

            except Exception:
                continue

        raise RuntimeError(
            (
                "A rotina foi acionada, mas "
                "a janela de fechamento fiscal "
                "não foi identificada."
            )
        )

    # ========================================================
    # LOCALIZAR CAMPO NOVA DATA
    #
    # O INPUT DO PROTHEUS ESTÁ DENTRO DE:
    #
    # #shadow-root (open)
    #     <input type="text">
    #
    # Os seletores CSS do Playwright atravessam Shadow DOM
    # aberto. Por isso procuramos todos os INPUTS visíveis
    # e escolhemos o que está imediatamente à direita
    # do texto "Nova data".
    # ========================================================

    def localizar_campo_nova_data(
        self,
    ) -> Locator:

        for contexto in self._contextos():

            # =================================================
            # LOCALIZA O RÓTULO
            # =================================================

            try:

                rotulos = (
                    contexto.get_by_text(
                        "Nova data",
                        exact=False,
                    )
                )

            except Exception:
                continue

            for indice_rotulo in range(
                rotulos.count()
            ):

                rotulo = (
                    rotulos.nth(
                        indice_rotulo
                    )
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

                # =================================================
                # IMPORTANTE:
                #
                # CSS LOCATOR ATRAVESSA SHADOW DOM OPEN
                # =================================================

                try:

                    inputs = contexto.locator(
                        "input:visible"
                    )

                except Exception:
                    continue

                melhor_input = None
                melhor_distancia = None

                centro_rotulo_x = (
                    caixa_rotulo["x"]
                    + (
                        caixa_rotulo["width"]
                        / 2
                    )
                )

                centro_rotulo_y = (
                    caixa_rotulo["y"]
                    + (
                        caixa_rotulo["height"]
                        / 2
                    )
                )

                for indice_input in range(
                    inputs.count()
                ):

                    input_atual = (
                        inputs.nth(
                            indice_input
                        )
                    )

                    try:

                        if not input_atual.is_visible():
                            continue

                        caixa_input = (
                            input_atual.bounding_box()
                        )

                        if caixa_input is None:
                            continue

                    except Exception:
                        continue

                    centro_input_x = (
                        caixa_input["x"]
                        + (
                            caixa_input["width"]
                            / 2
                        )
                    )

                    centro_input_y = (
                        caixa_input["y"]
                        + (
                            caixa_input["height"]
                            / 2
                        )
                    )

                    # ==========================================
                    # PRECISA ESTAR À DIREITA DO "NOVA DATA"
                    # ==========================================

                    distancia_x = (
                        centro_input_x
                        - centro_rotulo_x
                    )

                    distancia_y = abs(
                        centro_input_y
                        - centro_rotulo_y
                    )

                    # Campo precisa estar à direita.
                    if distancia_x < 0:
                        continue

                    # Não pode estar muito distante.
                    if distancia_x > 350:
                        continue

                    # Precisa estar praticamente
                    # na mesma linha.
                    if distancia_y > 50:
                        continue

                    distancia = (
                        distancia_x
                        + distancia_y
                    )

                    if (
                        melhor_distancia is None
                        or distancia
                        < melhor_distancia
                    ):

                        melhor_distancia = (
                            distancia
                        )

                        melhor_input = (
                            input_atual
                        )

                if melhor_input is not None:

                    return melhor_input

        raise RuntimeError(
            (
                "A janela de fechamento foi aberta, "
                "mas o input da Nova data dentro do "
                "Shadow DOM não foi localizado."
            )
        )

    # ========================================================
    # OBTER VALOR REAL DO INPUT
    # ========================================================

    def _obter_valor_campo(
        self,
        campo: Locator,
    ) -> str:

        try:

            valor = campo.input_value()

            if valor is not None:
                return str(valor)

        except Exception:
            pass

        try:

            valor = campo.evaluate(
                """
                element => {
                    if ('value' in element) {
                        return element.value;
                    }

                    return '';
                }
                """
            )

            if valor is not None:
                return str(valor)

        except Exception:
            pass

        return ""

    # ========================================================
    # PREENCHER NOVA DATA
    #
    # INTERAÇÃO DE TECLADO
    #
    # NÃO CLICA EM OK.
    # ========================================================

    def preencher_nova_data(
        self,
        nova_data: str,
    ):

        campo = (
            self.localizar_campo_nova_data()
        )

        # ====================================================
        # FOCO
        # ====================================================

        campo.click()

        self.page.wait_for_timeout(
            400
        )

        # ====================================================
        # CTRL+A
        # ====================================================

        campo.press(
            "Control+A"
        )

        self.page.wait_for_timeout(
            250
        )

        # ====================================================
        # APAGA O VALOR ANTIGO
        # ====================================================

        campo.press(
            "Backspace"
        )

        self.page.wait_for_timeout(
            300
        )

        # ====================================================
        # DIGITAÇÃO HUMANA
        #
        # Exemplo:
        #
        # 3
        # 1
        # /
        # 0
        # 1
        # /
        # 2
        # 0
        # 2
        # 6
        # ====================================================

        campo.press_sequentially(
            nova_data,
            delay=120,
        )

        self.page.wait_for_timeout(
            500
        )

        # ====================================================
        # TAB
        #
        # O componente processa a máscara.
        # ====================================================

        campo.press(
            "Tab"
        )

        self.page.wait_for_timeout(
            1000
        )

        # ====================================================
        # CONFERE O VALOR
        # ====================================================

        valor_atual = (
            self._obter_valor_campo(
                campo
            )
        )

        numeros_atual = (
            self._somente_numeros(
                valor_atual
            )
        )

        numeros_esperado = (
            self._somente_numeros(
                nova_data
            )
        )

        if (
            numeros_atual
            != numeros_esperado
        ):

            raise RuntimeError(
                (
                    "O robô localizou o campo Nova data "
                    "e realizou a digitação, porém o valor "
                    "final não corresponde à competência.\n\n"
                    f"Esperado: {nova_data}\n"
                    f"Encontrado: {valor_atual}\n\n"
                    "O fechamento NÃO foi confirmado."
                )
            )

        # ====================================================
        # SEGURANÇA
        #
        # NÃO HÁ CLIQUE EM OK.
        # ====================================================

        return valor_atual
