from database.connection import Base, engine

from models.entities import Credencial


def executar():

    print()
    print("=" * 60)
    print("CRIANDO TABELA DE CREDENCIAIS")
    print("=" * 60)

    Base.metadata.create_all(
        bind=engine
    )

    print()
    print("[OK] Estrutura de credenciais verificada.")
    print("[OK] Tabela credenciais criada, se não existia.")
    print()


if __name__ == "__main__":
    executar()
