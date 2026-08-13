from datetime import datetime

from database.connection import SessionLocal
from models.entities import TaskExecution


class TaskExecutionRepository:

    def listar(self):
        with SessionLocal() as session:
            return (
                session.query(TaskExecution)
                .order_by(
                    TaskExecution.id.desc()
                )
                .all()
            )

    def listar_por_competencia(
        self,
        competencia_id,
    ):
        with SessionLocal() as session:
            return (
                session.query(TaskExecution)
                .filter(
                    TaskExecution.competencia_id
                    == competencia_id
                )
                .order_by(
                    TaskExecution.id
                )
                .all()
            )

    def buscar_por_id(
        self,
        execution_id,
    ):
        with SessionLocal() as session:
            return (
                session.query(TaskExecution)
                .filter(
                    TaskExecution.id
                    == execution_id
                )
                .first()
            )

    def buscar_tarefa(
        self,
        competencia_id,
        task_key,
    ):
        with SessionLocal() as session:
            return (
                session.query(TaskExecution)
                .filter(
                    TaskExecution.competencia_id
                    == competencia_id,
                    TaskExecution.task_key
                    == task_key,
                )
                .order_by(
                    TaskExecution.id.desc()
                )
                .first()
            )

    def criar(
        self,
        competencia_id,
        task_key,
        task_name,
    ):
        with SessionLocal() as session:

            execucao = TaskExecution(
                competencia_id=competencia_id,
                task_key=task_key,
                task_name=task_name,
                status="PENDENTE",
            )

            session.add(
                execucao
            )

            session.commit()

            session.refresh(
                execucao
            )

            return execucao

    def iniciar(
        self,
        execution_id,
    ):
        with SessionLocal() as session:

            execucao = (
                session.query(TaskExecution)
                .filter(
                    TaskExecution.id
                    == execution_id
                )
                .first()
            )

            if execucao is None:
                return None

            execucao.status = "EM_EXECUCAO"
            execucao.started_at = datetime.now()
            execucao.finished_at = None
            execucao.last_error = None

            session.commit()

            session.refresh(
                execucao
            )

            return execucao

    def atualizar_status(
        self,
        execution_id,
        status,
        erro=None,
    ):
        with SessionLocal() as session:

            execucao = (
                session.query(TaskExecution)
                .filter(
                    TaskExecution.id
                    == execution_id
                )
                .first()
            )

            if execucao is None:
                return None

            execucao.status = status

            if erro:
                execucao.last_error = str(
                    erro
                )

            if status == "CONCLUIDO":
                execucao.finished_at = (
                    datetime.now()
                )

            session.commit()

            session.refresh(
                execucao
            )

            return execucao
