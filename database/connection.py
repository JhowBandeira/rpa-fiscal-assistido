from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "rpa_fiscal.db"

class Base(DeclarativeBase):
    pass

engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    from models.entities import Empresa, Filial, InscricaoEstadual, InscricaoMunicipal, Competencia, TaskExecution, Checkpoint
    Base.metadata.create_all(engine)
