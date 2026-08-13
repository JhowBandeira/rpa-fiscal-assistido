import json

from datetime import datetime

from database.connection import SessionLocal
from models.entities import Checkpoint


class CheckpointRepository:

    def buscar_por_execucao(
        self,
        execution_id,
    ):
        with SessionLocal() as session:
            return (
                session.query(Checkpoint)
                .filter(
                    Checkpoint.execution_id
                    == execution_id
                )
                .first()
            )

    def salvar(
        self,
        execution_id,
        step_key,
        item_key=None,
        payload=None,
    ):
        with SessionLocal() as session:

            checkpoint = (
                session.query(Checkpoint)
                .filter(
                    Checkpoint.execution_id
                    == execution_id
                )
                .first()
            )

            payload_json = None

            if payload is not None:
                payload_json = json.dumps(
                    payload,
                    ensure_ascii=False,
                )

            if checkpoint is None:

                checkpoint = Checkpoint(
                    execution_id=execution_id,
                    step_key=step_key,
                    item_key=item_key,
                    payload_json=payload_json,
                    updated_at=datetime.now(),
                )

                session.add(
                    checkpoint
                )

            else:

                checkpoint.step_key = step_key
                checkpoint.item_key = item_key
                checkpoint.payload_json = payload_json
                checkpoint.updated_at = datetime.now()

            session.commit()

            session.refresh(
                checkpoint
            )

            return checkpoint

    def carregar_payload(
        self,
        execution_id,
    ):
        checkpoint = (
            self.buscar_por_execucao(
                execution_id
            )
        )

        if checkpoint is None:
            return None

        if not checkpoint.payload_json:
            return {}

        try:
            return json.loads(
                checkpoint.payload_json
            )

        except json.JSONDecodeError:
            return {}

    def excluir(
        self,
        execution_id,
    ):
        with SessionLocal() as session:

            checkpoint = (
                session.query(Checkpoint)
                .filter(
                    Checkpoint.execution_id
                    == execution_id
                )
                .first()
            )

            if checkpoint is None:
                return False

            session.delete(
                checkpoint
            )

            session.commit()

            return True
