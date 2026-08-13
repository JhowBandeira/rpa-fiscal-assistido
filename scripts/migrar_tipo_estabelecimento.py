from pathlib import Path

from sqlalchemy import inspect, text

from database.connection import engine


def mostrar_banco():
    print()
    print("=" * 70)
    print("BANCO UTILIZADO")
    print("=" * 70)

    print(f"URL: {engine.url}")

    if engine.url.database:
        caminho = Path(engine.url.database).resolve()
        print(f"Arquivo: {caminho}")

    print()


def coluna_existe(nome_coluna):
    inspector = inspect(engine)

    colunas = inspector.get_columns(
        "filiais"
    )

    nomes = [
        coluna["name"]
        for coluna in colunas
    ]

    return nome_coluna in nomes


def listar_colunas():
    inspector = inspect(engine)

    colunas = inspector.get_columns(
        "filiais"
    )

    print()
    print("COLUNAS DA TABELA FILIAIS:")

    for coluna in colunas:
        print(
            f" - {coluna['name']}"
        )

    print()


def criar_coluna_tipo():
    if coluna_existe("tipo"):
        print(
            "[OK] A coluna 'tipo' já existe."
        )
        return

    print(
        "[AÇÃO] Criando coluna 'tipo'..."
    )

    with engine.begin() as conexao:
        conexao.execute(
            text(
                """
                ALTER TABLE filiais
                ADD COLUMN tipo VARCHAR(20)
                DEFAULT 'FILIAL'
                """
            )
        )

    print(
        "[OK] Coluna 'tipo' criada."
    )


def atualizar_estabelecimentos():
    print()
    print(
        "[AÇÃO] Atualizando MATRIZ e FILIAIS..."
    )

    with engine.begin() as conexao:

        # ==========================================
        # MATRIZ - DIADEMA
        # ==========================================

        conexao.execute(
            text(
                """
                UPDATE filiais
                SET tipo = 'MATRIZ'
                WHERE REPLACE(
                    REPLACE(
                        REPLACE(
                            cnpj,
                            '.',
                            ''
                        ),
                        '/',
                        ''
                    ),
                    '-',
                    ''
                ) = '03972433000105'
                """
            )
        )

        # ==========================================
        # CONTAGEM
        # ==========================================

        conexao.execute(
            text(
                """
                UPDATE filiais
                SET tipo = 'FILIAL'
                WHERE REPLACE(
                    REPLACE(
                        REPLACE(
                            cnpj,
                            '.',
                            ''
                        ),
                        '/',
                        ''
                    ),
                    '-',
                    ''
                ) = '03972433001179'
                """
            )
        )

        # ==========================================
        # SÃO BERNARDO
        # ==========================================

        conexao.execute(
            text(
                """
                UPDATE filiais
                SET tipo = 'FILIAL'
                WHERE REPLACE(
                    REPLACE(
                        REPLACE(
                            cnpj,
                            '.',
                            ''
                        ),
                        '/',
                        ''
                    ),
                    '-',
                    ''
                ) = '03972433001330'
                """
            )
        )

        # ==========================================
        # JOINVILLE
        # ==========================================

        conexao.execute(
            text(
                """
                UPDATE filiais
                SET tipo = 'FILIAL'
                WHERE REPLACE(
                    REPLACE(
                        REPLACE(
                            cnpj,
                            '.',
                            ''
                        ),
                        '/',
                        ''
                    ),
                    '-',
                    ''
                ) = '03972433001098'
                """
            )
        )

    print(
        "[OK] Estabelecimentos atualizados."
    )


def mostrar_resultado():
    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)

    with engine.connect() as conexao:
        resultado = conexao.execute(
            text(
                """
                SELECT
                    id,
                    identificacao,
                    cnpj,
                    uf,
                    tipo
                FROM filiais
                ORDER BY identificacao
                """
            )
        )

        registros = resultado.fetchall()

    for registro in registros:
        print(
            f"{registro.identificacao} | "
            f"{registro.cnpj} | "
            f"{registro.uf} | "
            f"{registro.tipo}"
        )

    print()


def executar():
    print()
    print("=" * 70)
    print("MIGRAÇÃO - TIPO DO ESTABELECIMENTO")
    print("=" * 70)

    mostrar_banco()

    listar_colunas()

    criar_coluna_tipo()

    if not coluna_existe("tipo"):
        raise RuntimeError(
            "A coluna 'tipo' não foi criada."
        )

    atualizar_estabelecimentos()

    listar_colunas()

    mostrar_resultado()

    print("=" * 70)
    print("MIGRAÇÃO CONCLUÍDA COM SUCESSO")
    print("=" * 70)
    print()


if __name__ == "__main__":
    executar()
