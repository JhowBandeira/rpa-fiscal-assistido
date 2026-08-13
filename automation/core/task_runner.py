from datetime import datetime
import json
from database.connection import SessionLocal
from models.entities import TaskExecution, Checkpoint

WAITING_TRAINING = "AGUARDANDO_TREINAMENTO"

class TaskRunner:
    def create_execution(self, competencia_id: int, task_key: str, task_name: str) -> int:
        with SessionLocal() as db:
            row = TaskExecution(competencia_id=competencia_id, task_key=task_key, task_name=task_name, status="PENDENTE")
            db.add(row); db.commit(); db.refresh(row)
            cp = Checkpoint(execution_id=row.id, step_key="inicio")
            db.add(cp); db.commit()
            return row.id

    def checkpoint(self, execution_id: int, step_key: str, item_key=None, payload=None):
        with SessionLocal() as db:
            cp = db.query(Checkpoint).filter_by(execution_id=execution_id).one()
            cp.step_key = step_key
            cp.item_key = item_key
            cp.payload_json = json.dumps(payload or {}, ensure_ascii=False)
            cp.updated_at = datetime.utcnow()
            db.commit()

    def resume_state(self, execution_id: int):
        with SessionLocal() as db:
            cp = db.query(Checkpoint).filter_by(execution_id=execution_id).one()
            return {"step_key": cp.step_key, "item_key": cp.item_key, "payload": json.loads(cp.payload_json or "{}")}

    def set_status(self, execution_id: int, status: str, error: str | None = None):
        with SessionLocal() as db:
            ex = db.get(TaskExecution, execution_id)
            ex.status = status
            ex.last_error = error
            if status == "EM_EXECUCAO" and not ex.started_at:
                ex.started_at = datetime.utcnow()
            if status in {"CONCLUIDO", "ERRO"}:
                ex.finished_at = datetime.utcnow()
            db.commit()
