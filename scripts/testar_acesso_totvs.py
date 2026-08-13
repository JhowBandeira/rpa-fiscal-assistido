from rpa.totvs_access import (
    TotvsAccess,
)


def executar():

    print()
    print("=" * 70)
    print("TESTE DE LOGIN DO TOTVS")
    print("=" * 70)

    totvs = TotvsAccess()

    try:

        # ====================================================
        # CREDENCIAL
        # ====================================================

        print()
        print(
            "[1/4] Verificando credencial..."
        )

        totvs.validar_credencial()

        print(
            "[OK] Credencial encontrada."
        )

        # ====================================================
        # ABRIR E LOGAR
        # ====================================================

        print()
        print(
            "[2/4] Abrindo TOTVS..."
        )

        print(
            "[3/4] Preenchendo acesso..."
        )

        print(
            "[4/4] Efetuando login..."
        )

        page = (
            totvs.fazer_login()
        )

        if page is None:

            raise RuntimeError(
                (
                    "O login foi executado, "
                    "mas nenhuma página foi retornada."
                )
            )

        # ====================================================
        # RESULTADO
        # ====================================================

        print()
        print("=" * 70)
        print("LOGIN EXECUTADO")
        print("=" * 70)

        print()
        print(
            "O robô enviou o acesso ao TOTVS."
        )

        print()
        print(
            "A próxima tela ainda NÃO será automatizada."
        )

        print(
            "Precisamos ensiná-la primeiro."
        )

        print()
        print(
            f"Título atual: {page.title()}"
        )

        print()
        print(
            f"Endereço atual: {page.url}"
        )

        print()
        print("=" * 70)
        print("AGUARDANDO PRÓXIMO PASSO")
        print("=" * 70)

        print()
        print(
            (
                "Confira a tela aberta no Chrome "
                "e envie um print dela."
            )
        )

        print()
        print(
            (
                "Não envie usuário ou senha. "
                "Eles já estão armazenados localmente."
            )
        )

        print()

        input(
            (
                "Pressione ENTER somente quando "
                "quiser fechar o navegador..."
            )
        )

    except Exception as erro:

        print()
        print("=" * 70)
        print("ERRO")
        print("=" * 70)

        print()
        print(
            str(erro)
        )

        print()

        input(
            "Pressione ENTER para finalizar..."
        )

    finally:

        totvs.fechar()


if __name__ == "__main__":
    executar()
