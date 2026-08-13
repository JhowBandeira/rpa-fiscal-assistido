from rpa.totvs_access import (
    TotvsAccess,
)

from rpa.totvs_navigation import (
    TotvsNavigation,
)


# ============================================================
# ESCOLHA A FILIAL PARA O TESTE
#
# DIADEMA
# CNPJ_ESTABELECIMENTO = "03972433000105"
#
# CONTAGEM
CNPJ_ESTABELECIMENTO = "03972433001179"
#
# SÃO BERNARDO DO CAMPO
# CNPJ_ESTABELECIMENTO = "03972433001330"
#
# JOINVILLE
# CNPJ_ESTABELECIMENTO = "03972433001098"
# ============================================================


def executar():

    print()
    print("=" * 75)
    print("TESTE COMPLETO - FECHAR PERÍODO")
    print("MODO SEGURO: NÃO EFETUA O FECHAMENTO")
    print("=" * 75)

    totvs = TotvsAccess()

    try:

        # ====================================================
        # 1. LOGIN
        # ====================================================

        print()
        print("[1/9] Efetuando login no TOTVS...")

        page = totvs.fazer_login()

        navegacao = TotvsNavigation(
            page
        )

        print("[OK] Login realizado.")

        # ====================================================
        # 2. TELA DE SELEÇÃO
        # ====================================================

        print()
        print("[2/9] Aguardando tela de seleção...")

        page.wait_for_timeout(
            3000
        )

        navegacao.aguardar_texto(
            "Grupo",
            timeout_ms=30000,
        )

        navegacao.aguardar_texto(
            "Filial",
            timeout_ms=30000,
        )

        navegacao.aguardar_texto(
            "Ambiente",
            timeout_ms=30000,
        )

        print("[OK] Tela de seleção localizada.")

        print()
        print("      Data base: NÃO SERÁ ALTERADA.")
        print("      Grupo: NÃO SERÁ ALTERADO.")

        # ====================================================
        # 3. ABRIR FILIAL
        # ====================================================

        print()
        print("[3/9] Abrindo pesquisa da Filial...")

        navegacao.clicar_lupa_campo(
            "Filial"
        )

        print("[OK] Pesquisa de filial aberta.")

        # ====================================================
        # 4. SELECIONAR FILIAL PELO CNPJ
        # ====================================================

        print()
        print(
            "[4/9] Selecionando estabelecimento "
            f"pelo CNPJ {CNPJ_ESTABELECIMENTO}..."
        )

        navegacao.selecionar_filial_por_cnpj(
            CNPJ_ESTABELECIMENTO
        )

        print("[OK] Estabelecimento confirmado.")

        # ====================================================
        # 5. AMBIENTE
        # ====================================================

        print()
        print("[5/9] Abrindo pesquisa de Ambiente...")

        navegacao.clicar_lupa_campo(
            "Ambiente"
        )

        print("[OK] Pesquisa de ambiente aberta.")

        # ====================================================
        # 6. LIVROS FISCAIS
        # ====================================================

        print()
        print("[6/9] Selecionando 9 - Livros Fiscais...")

        navegacao.selecionar_ambiente_livros_fiscais()

        print("[OK] Livros Fiscais confirmado.")

        # ====================================================
        # 7. ENTRAR
        # ====================================================

        print()
        print("[7/9] Entrando em Livros Fiscais...")

        navegacao.entrar_no_ambiente()

        print("[OK] Ambiente Livros Fiscais aberto.")

        # ====================================================
        # 8. MISCELÂNEA > ACERTOS
        # ====================================================

        print()
        print("[8/9] Abrindo Miscelânea > Acertos...")

        navegacao.abrir_miscelanea()

        navegacao.abrir_acertos()

        print("[OK] Menu Acertos aberto.")

        # ====================================================
        # 9. DATA FECH/TO FISCAL
        # ====================================================

        print()
        print("[9/9] Abrindo Data Fech/to Fiscal...")

        navegacao.abrir_data_fechamento_fiscal()

        navegacao.confirmar_tela_fechamento()

        # ====================================================
        # PARADA SEGURA
        # ====================================================

        print()
        print()
        print("=" * 75)
        print("TESTE CONCLUÍDO COM SEGURANÇA")
        print("=" * 75)

        print()
        print(
            "O robô chegou à tela de fechamento fiscal."
        )

        print()
        print("NENHUM FECHAMENTO FOI REALIZADO.")
        print()
        print("- Data base não foi alterada.")
        print("- Grupo não foi alterado.")
        print("- Nova data não foi alterada.")
        print("- O botão OK não foi clicado.")

        print()
        print(
            "Confira se a filial exibida no topo "
            "do TOTVS é a filial testada."
        )

        print()
        print(
            "O navegador continuará aberto "
            "para conferência."
        )

        print()

        input(
            (
                "Pressione ENTER somente quando "
                "quiser encerrar o teste..."
            )
        )

    except Exception as erro:

        print()
        print("=" * 75)
        print("ERRO DURANTE O TESTE")
        print("=" * 75)
        print()
        print(str(erro))
        print()

        print(
            "Nenhum fechamento será confirmado "
            "automaticamente por este teste."
        )

        print()

        input(
            "Pressione ENTER para finalizar..."
        )

    finally:

        totvs.fechar()


if __name__ == "__main__":
    executar()
