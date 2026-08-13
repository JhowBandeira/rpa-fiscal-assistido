from rpa.totvs_access import TotvsAccess


def texto_seguro(valor):
    if valor is None:
        return ""

    valor = str(valor)

    if len(valor) > 120:
        return valor[:120] + "..."

    return valor


def inspecionar_contexto(contexto, nome):

    print()
    print("=" * 80)
    print(f"CONTEXTO: {nome}")
    print("=" * 80)

    # ========================================================
    # INPUTS
    # ========================================================

    try:
        inputs = contexto.locator("input")

        print()
        print(f"INPUTS ENCONTRADOS: {inputs.count()}")
        print()

        for indice in range(inputs.count()):

            elemento = inputs.nth(indice)

            try:
                if not elemento.is_visible():
                    continue
            except Exception:
                continue

            tipo = elemento.get_attribute("type") or ""
            nome_input = elemento.get_attribute("name") or ""
            elemento_id = elemento.get_attribute("id") or ""
            placeholder = elemento.get_attribute("placeholder") or ""
            aria_label = elemento.get_attribute("aria-label") or ""

            if tipo.lower() == "password":
                valor = "[OCULTO]"
            else:
                try:
                    valor = elemento.input_value()
                except Exception:
                    valor = ""

            print(
                f"[INPUT {indice}] "
                f"type={texto_seguro(tipo)!r} | "
                f"name={texto_seguro(nome_input)!r} | "
                f"id={texto_seguro(elemento_id)!r} | "
                f"placeholder={texto_seguro(placeholder)!r} | "
                f"aria-label={texto_seguro(aria_label)!r} | "
                f"value={texto_seguro(valor)!r}"
            )

    except Exception as erro:

        print(
            f"Não foi possível inspecionar inputs: {erro}"
        )

    # ========================================================
    # BOTÕES
    # ========================================================

    try:
        botoes = contexto.locator("button")

        print()
        print(f"BOTÕES ENCONTRADOS: {botoes.count()}")
        print()

        for indice in range(botoes.count()):

            elemento = botoes.nth(indice)

            try:
                if not elemento.is_visible():
                    continue
            except Exception:
                continue

            elemento_id = elemento.get_attribute("id") or ""
            classe = elemento.get_attribute("class") or ""
            titulo = elemento.get_attribute("title") or ""
            aria_label = elemento.get_attribute("aria-label") or ""

            try:
                texto = elemento.inner_text()
            except Exception:
                texto = ""

            print(
                f"[BOTÃO {indice}] "
                f"text={texto_seguro(texto)!r} | "
                f"id={texto_seguro(elemento_id)!r} | "
                f"title={texto_seguro(titulo)!r} | "
                f"aria-label={texto_seguro(aria_label)!r} | "
                f"class={texto_seguro(classe)!r}"
            )

    except Exception as erro:

        print(
            f"Não foi possível inspecionar botões: {erro}"
        )


def executar():

    print()
    print("=" * 80)
    print("INSPEÇÃO DA TELA DE SELEÇÃO DO TOTVS")
    print("=" * 80)

    totvs = TotvsAccess()

    try:

        print()
        print("[1/2] Efetuando login...")

        page = totvs.fazer_login()

        print("[OK] Login enviado.")

        print()
        print(
            "[2/2] Aguardando tela de Grupo / Filial / Ambiente..."
        )

        page.wait_for_timeout(
            5000
        )

        # ====================================================
        # PÁGINA PRINCIPAL
        # ====================================================

        inspecionar_contexto(
            page,
            "PÁGINA PRINCIPAL",
        )

        # ====================================================
        # FRAMES
        # ====================================================

        for indice, frame in enumerate(
            page.frames
        ):

            if frame == page.main_frame:
                continue

            try:
                endereco = frame.url
            except Exception:
                endereco = ""

            inspecionar_contexto(
                frame,
                (
                    f"FRAME {indice} "
                    f"- {endereco}"
                ),
            )

        print()
        print("=" * 80)
        print("INSPEÇÃO CONCLUÍDA")
        print("=" * 80)
        print()
        print(
            "O navegador ficará aberto para conferência."
        )
        print()

        input(
            "Pressione ENTER somente quando quiser fechar..."
        )

    except Exception as erro:

        print()
        print("=" * 80)
        print("ERRO")
        print("=" * 80)
        print()
        print(str(erro))
        print()

        input(
            "Pressione ENTER para finalizar..."
        )

    finally:

        totvs.fechar()


if __name__ == "__main__":
    executar()
