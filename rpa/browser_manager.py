from playwright.sync_api import (
    sync_playwright,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)


class BrowserManager:

    def __init__(self):

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def iniciar(self) -> Page:

        if self.page is not None:
            return self.page

        self.playwright = sync_playwright().start()

        # ====================================================
        # TENTA ABRIR O GOOGLE CHROME INSTALADO NO WINDOWS
        # ====================================================

        try:

            self.browser = (
                self.playwright.chromium.launch(
                    headless=False,
                    channel="chrome",
                    args=[
                        "--start-maximized",
                    ],
                )
            )

        except Exception:

            # =================================================
            # FALLBACK PARA O CHROMIUM DO PLAYWRIGHT
            # =================================================

            self.browser = (
                self.playwright.chromium.launch(
                    headless=False,
                    args=[
                        "--start-maximized",
                    ],
                )
            )

        if self.browser is None:

            raise RuntimeError(
                "Não foi possível iniciar o navegador."
            )

        self.context = (
            self.browser.new_context(
                viewport=None,
            )
        )

        if self.context is None:

            raise RuntimeError(
                "Não foi possível criar o contexto do navegador."
            )

        self.page = (
            self.context.new_page()
        )

        if self.page is None:

            raise RuntimeError(
                "Não foi possível criar a página do navegador."
            )

        return self.page

    def abrir_url(
        self,
        url: str,
    ) -> Page:

        page = self.iniciar()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        return page

    def pagina_atual(
        self,
    ) -> Page | None:

        return self.page

    def fechar(self):

        try:

            if self.context is not None:
                self.context.close()

        except Exception:
            pass

        try:

            if self.browser is not None:
                self.browser.close()

        except Exception:
            pass

        try:

            if self.playwright is not None:
                self.playwright.stop()

        except Exception:
            pass

        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
