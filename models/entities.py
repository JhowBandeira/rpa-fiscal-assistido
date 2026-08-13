from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from database.connection import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    razao_social: Mapped[str] = mapped_column(
        String(180)
    )

    nome_fantasia: Mapped[str | None] = mapped_column(
        String(180),
        nullable=True,
    )

    cnpj: Mapped[str] = mapped_column(
        String(18),
        unique=True,
        index=True,
    )

    diretorio_base: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


class Filial(Base):
    __tablename__ = "filiais"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
    )

    identificacao: Mapped[str] = mapped_column(
        String(120)
    )

    cnpj: Mapped[str] = mapped_column(
        String(18),
        index=True,
    )

    uf: Mapped[str] = mapped_column(
        String(2)
    )

    municipio: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(20),
        default="FILIAL",
    )


class InscricaoEstadual(Base):
    __tablename__ = "inscricoes_estaduais"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
    )

    filial_id: Mapped[int | None] = mapped_column(
        ForeignKey("filiais.id"),
        nullable=True,
    )

    uf: Mapped[str] = mapped_column(
        String(2)
    )

    numero: Mapped[str] = mapped_column(
        String(40)
    )

    emitir_cnd: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


class InscricaoMunicipal(Base):
    __tablename__ = "inscricoes_municipais"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
    )

    filial_id: Mapped[int | None] = mapped_column(
        ForeignKey("filiais.id"),
        nullable=True,
    )

    municipio: Mapped[str] = mapped_column(
        String(120)
    )

    uf: Mapped[str] = mapped_column(
        String(2)
    )

    numero: Mapped[str] = mapped_column(
        String(60)
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


class Competencia(Base):
    __tablename__ = "competencias"

    __table_args__ = (
        UniqueConstraint(
            "empresa_id",
            "filial_id",
            "mes",
            "ano",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        index=True,
    )

    filial_id: Mapped[int | None] = mapped_column(
        ForeignKey("filiais.id"),
        nullable=True,
    )

    mes: Mapped[int] = mapped_column(
        Integer
    )

    ano: Mapped[int] = mapped_column(
        Integer
    )

    data_entrega: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    data_vencimento: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(40),
        default="PENDENTE",
    )


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    competencia_id: Mapped[int] = mapped_column(
        ForeignKey("competencias.id"),
        index=True,
    )

    task_key: Mapped[str] = mapped_column(
        String(80),
        index=True,
    )

    task_name: Mapped[str] = mapped_column(
        String(180)
    )

    status: Mapped[str] = mapped_column(
        String(40),
        default="PENDENTE",
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    last_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


class Checkpoint(Base):
    __tablename__ = "checkpoints"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    execution_id: Mapped[int] = mapped_column(
        ForeignKey("task_executions.id"),
        unique=True,
        index=True,
    )

    step_key: Mapped[str] = mapped_column(
        String(120),
        default="inicio",
    )

    item_key: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    payload_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Credencial(Base):
    __tablename__ = "credenciais"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    sistema: Mapped[str] = mapped_column(
        String(80),
        index=True,
    )

    tipo_vinculo: Mapped[str] = mapped_column(
        String(30),
        default="GLOBAL",
    )

    empresa_id: Mapped[int | None] = mapped_column(
        ForeignKey("empresas.id"),
        nullable=True,
        index=True,
    )

    filial_id: Mapped[int | None] = mapped_column(
        ForeignKey("filiais.id"),
        nullable=True,
        index=True,
    )

    usuario: Mapped[str] = mapped_column(
        String(180)
    )

    chave_cofre: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        index=True,
    )

    ativa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
