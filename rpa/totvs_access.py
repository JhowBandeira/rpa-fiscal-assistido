from playwright.sync_api import (
    Page,
    Locator,
    TimeoutError as PlaywrightTimeoutError,
)

from services.credencial_service import (
    CredencialService,
)

from rpa.browser_manager import (
    BrowserManager,
)


class TotvsAccess:

    def __init__(self):

        self.credencial_service = (
            CredencialService()
        )

        self.browser_manager = (
            BrowserManager()
        )

    # ========================================================
    # CREDENCIAL
    # ========================================================

    def validar_credencial(self):

        acesso = (
            self.credencial_service
            .obter_para_execucao(
                sistema="TOTVS"
            )
        )

        if acesso is None:

            raise RuntimeError(
                (
                    "Não existe uma credencial "
                    "GLOBAL do TOTVS cadastrada."
                )
            )

        if not acesso.get("usuario"):

            raise RuntimeError(
                (
                    "A credencial do TOTVS "
                    "não possui usuário."
                )
            )

        if not acesso.get("senha"):

            raise RuntimeError(
                (
                    "A senha do TOTVS não foi "
                    "localizada no cofre do Windows."
                )
            )

        return acesso

    # ========================================================
    # ABRIR TOTVS
    # ========================================================

    def abrir_tela_login(self) -> Page:

        acesso = (
            self.validar_credencial()
        )

        url = acesso["url"]

        page = (
            self.browser_manager
            .abrir_url(
                url
            )
        )

        page.wait_for_timeout(
            2500
        )

        return page

    # ========================================================
    # LOCALIZAR USUÁRIO
    # ========================================================

    def _localizar_campo_usuario(
        self,
        page: Page,
    ) -> Locator:

        # ----------------------------------------------------
        # PÁGINA PRINCIPAL
        # ----------------------------------------------------

        candidatos = [
            page.get_by_label(
                "Insira seu usuário",
                exact=False,
            ),
            page.locator(
                'input[type="text"]:visible'
            ),
            page.locator(
                "input:visible"
            ),
        ]

        for candidato in candidatos:

            try:

                quantidade = candidato.count()

                if quantidade > 0:

                    for indice in range(
                        quantidade
                    ):

                        item = candidato.nth(
                            indice
                        )

                        if item.is_visible():

                            return item

            except Exception:
                pass

        # ----------------------------------------------------
        # FRAMES
        # ----------------------------------------------------

        for frame in page.frames:

            try:

                candidatos_frame = [
                    frame.get_by_label(
                        "Insira seu usuário",
                        exact=False,
                    ),
                    frame.locator(
                        'input[type="text"]:visible'
                    ),
                    frame.locator(
                        "input:visible"
                    ),
                ]

                for candidato in candidatos_frame:

                    quantidade = (
                        candidato.count()
                    )

                    if quantidade > 0:

                        for indice in range(
                            quantidade
                        ):

                            item = (
                                candidato.nth(
                                    indice
                                )
                            )

                            if (
                                item.is_visible()
                            ):

                                return item

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                "o campo de usuário do TOTVS."
            )
        )

    # ========================================================
    # LOCALIZAR SENHA
    # ========================================================

    def _localizar_campo_senha(
        self,
        page: Page,
    ) -> Locator:

        # ----------------------------------------------------
        # TENTA PELO TYPE PASSWORD
        # ----------------------------------------------------

        candidatos = [
            page.get_by_label(
                "Insira sua senha",
                exact=False,
            ),
            page.locator(
                'input[type="password"]:visible'
            ),
        ]

        for candidato in candidatos:

            try:

                quantidade = (
                    candidato.count()
                )

                if quantidade > 0:

                    for indice in range(
                        quantidade
                    ):

                        item = candidato.nth(
                            indice
                        )

                        if item.is_visible():

                            return item

            except Exception:
                pass

        # ----------------------------------------------------
        # FRAMES
        # ----------------------------------------------------

        for frame in page.frames:

            try:

                candidatos_frame = [
                    frame.get_by_label(
                        "Insira sua senha",
                        exact=False,
                    ),
                    frame.locator(
                        'input[type="password"]:visible'
                    ),
                ]

                for candidato in candidatos_frame:

                    quantidade = (
                        candidato.count()
                    )

                    if quantidade > 0:

                        for indice in range(
                            quantidade
                        ):

                            item = (
                                candidato.nth(
                                    indice
                                )
                            )

                            if (
                                item.is_visible()
                            ):

                                return item

            except Exception:
                continue

        # ----------------------------------------------------
        # FALLBACK:
        # SEGUNDO INPUT VISÍVEL
        #
        # TOTVS:
        # 1º = usuário
        # 2º = senha
        # ----------------------------------------------------

        try:

            inputs = page.locator(
                "input:visible"
            )

            quantidade = inputs.count()

            if quantidade >= 2:

                campo = inputs.nth(
                    1
                )

                if campo.is_visible():

                    return campo

        except Exception:
            pass

        # ----------------------------------------------------
        # FALLBACK EM FRAME
        # ----------------------------------------------------

        for frame in page.frames:

            try:

                inputs = frame.locator(
                    "input:visible"
                )

                quantidade = inputs.count()

                if quantidade >= 2:

                    campo = inputs.nth(
                        1
                    )

                    if campo.is_visible():

                        return campo

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                "o campo de senha do TOTVS."
            )
        )

    # ========================================================
    # LOCALIZAR BOTÃO ENTRAR
    # ========================================================

    def _localizar_botao_entrar(
        self,
        page: Page,
    ) -> Locator:

        candidatos = [
            page.get_by_role(
                "button",
                name="Entrar",
                exact=True,
            ),
            page.locator(
                'button:has-text("Entrar")'
            ),
            page.get_by_text(
                "Entrar",
                exact=True,
            ),
        ]

        for candidato in candidatos:

            try:

                quantidade = (
                    candidato.count()
                )

                if quantidade > 0:

                    for indice in range(
                        quantidade
                    ):

                        item = candidato.nth(
                            indice
                        )

                        if item.is_visible():

                            return item

            except Exception:
                pass

        # ----------------------------------------------------
        # FRAMES
        # ----------------------------------------------------

        for frame in page.frames:

            try:

                candidatos_frame = [
                    frame.get_by_role(
                        "button",
                        name="Entrar",
                        exact=True,
                    ),
                    frame.locator(
                        'button:has-text("Entrar")'
                    ),
                    frame.get_by_text(
                        "Entrar",
                        exact=True,
                    ),
                ]

                for candidato in candidatos_frame:

                    quantidade = (
                        candidato.count()
                    )

                    if quantidade > 0:

                        for indice in range(
                            quantidade
                        ):

                            item = (
                                candidato.nth(
                                    indice
                                )
                            )

                            if (
                                item.is_visible()
                            ):

                                return item

            except Exception:
                continue

        raise RuntimeError(
            (
                "Não foi possível localizar "
                "o botão Entrar do TOTVS."
            )
        )

    # ========================================================
    # PREENCHER LOGIN
    # ========================================================

    def preencher_login(
        self,
        page: Page,
    ):

        acesso = (
            self.validar_credencial()
        )

        usuario = acesso["usuario"]
        senha = acesso["senha"]

        campo_usuario = (
            self._localizar_campo_usuario(
                page
            )
        )

        campo_senha = (
            self._localizar_campo_senha(
                page
            )
        )

        # ----------------------------------------------------
        # USUÁRIO
        # ----------------------------------------------------

        campo_usuario.click()

        campo_usuario.fill(
            ""
        )

        campo_usuario.fill(
            usuario
        )

        page.wait_for_timeout(
            300
        )

        # ----------------------------------------------------
        # SENHA
        # ----------------------------------------------------

        campo_senha.click()

        campo_senha.fill(
            ""
        )

        campo_senha.fill(
            senha
        )

        page.wait_for_timeout(
            300
        )

    # ========================================================
    # ENTRAR
    # ========================================================

    def clicar_entrar(
        self,
        page: Page,
    ):

        botao = (
            self._localizar_botao_entrar(
                page
            )
        )

        try:

            botao.wait_for(
                state="visible",
                timeout=10000,
            )

        except PlaywrightTimeoutError:

            raise RuntimeError(
                (
                    "O botão Entrar não ficou "
                    "disponível para o robô."
                )
            )

        botao.click()

    # ========================================================
    # LOGIN COMPLETO
    # ========================================================

    def fazer_login(self) -> Page:

        page = (
            self.abrir_tela_login()
        )

        # ----------------------------------------------------
        # AGUARDA CARREGAMENTO
        # ----------------------------------------------------

        page.wait_for_timeout(
            2000
        )

        # ----------------------------------------------------
        # PREENCHE
        # ----------------------------------------------------

        self.preencher_login(
            page
        )

        page.wait_for_timeout(
            700
        )

        # ----------------------------------------------------
        # ENTRA
        # ----------------------------------------------------

        self.clicar_entrar(
            page
        )

        # ----------------------------------------------------
        # AGUARDA PROCESSAMENTO DO TOTVS
        # ----------------------------------------------------

        page.wait_for_timeout(
            5000
        )

        return page

    # ========================================================
    # FECHAR
    # ========================================================

    def fechar(self):

        self.browser_manager.fechar()
