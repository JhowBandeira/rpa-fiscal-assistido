from repositories.task_execution_repository import (
    TaskExecutionRepository,
)

from repositories.checkpoint_repository import (
    CheckpointRepository,
)


STATUS_VALIDOS = {
    "PENDENTE",
    "EM_EXECUCAO",
    "PAUSADO",
    "CONCLUIDO",
    "ERRO",
    "AGUARDANDO_TREINAMENTO",
    "INTERVENCAO_USUARIO",
}


class ExecutionService:

    def __init__(self):

        self.execution_repository = (
            TaskExecutionRepository()
        )

        self.checkpoint_repository = (
            CheckpointRepository()
        )

    def obter_ou_criar_execucao(
        self,
        competencia_id,
        task_key,
        task_name,
    ):

        if not competencia_id:
            raise ValueError(
                "Competência não informada."
            )

        if not task_key:
            raise ValueError(
                "A chave da tarefa é obrigatória."
            )

        existente = (
            self.execution_repository
            .buscar_tarefa(
                competencia_id,
                task_key,
            )
        )

        if existente:
            return existente

        return (
            self.execution_repository
            .criar(
                competencia_id=competencia_id,
                task_key=task_key,
                task_name=task_name,
            )
        )

    def iniciar(
        self,
        execution_id,
    ):

        execucao = (
            self.execution_repository
            .iniciar(
                execution_id
            )
        )

        if execucao is None:
            raise ValueError(
                "Execução não encontrada."
            )

        return execucao

    def salvar_checkpoint(
        self,
        execution_id,
        step_key,
        item_key=None,
        payload=None,
    ):

        if not execution_id:
            raise ValueError(
                "Execução não informada."
            )

        if not step_key:
            raise ValueError(
                "Etapa não informada."
            )

        return (
            self.checkpoint_repository
            .salvar(
                execution_id=execution_id,
                step_key=step_key,
                item_key=item_key,
                payload=payload,
            )
        )

    def obter_checkpoint(
        self,
        execution_id,
    ):

        return (
            self.checkpoint_repository
            .buscar_por_execucao(
                execution_id
            )
        )

    def obter_contexto_retomada(
        self,
        execution_id,
    ):

        checkpoint = (
            self.checkpoint_repository
            .buscar_por_execucao(
                execution_id
            )
        )

        if checkpoint is None:

            return {
                "possui_checkpoint": False,
                "step_key": None,
                "item_key": None,
                "payload": {},
            }

        payload = (
            self.checkpoint_repository
            .carregar_payload(
                execution_id
            )
        )

        return {
            "possui_checkpoint": True,
            "step_key": checkpoint.step_key,
            "item_key": checkpoint.item_key,
            "payload": payload,
        }

    def pausar(
        self,
        execution_id,
    ):

        return self.alterar_status(
            execution_id,
            "PAUSADO",
        )

    def marcar_erro(
        self,
        execution_id,
        erro,
    ):

        return self.alterar_status(
            execution_id,
            "ERRO",
            erro,
        )

    def aguardar_intervencao(
        self,
        execution_id,
        motivo=None,
    ):

        return self.alterar_status(
            execution_id,
            "INTERVENCAO_USUARIO",
            motivo,
        )

    def concluir(
        self,
        execution_id,
    ):

        execucao = (
            self.alterar_status(
                execution_id,
                "CONCLUIDO",
            )
        )

        self.checkpoint_repository.excluir(
            execution_id
        )

        return execucao

    def alterar_status(
        self,
        execution_id,
        status,
        erro=None,
    ):

        if status not in STATUS_VALIDOS:

            raise ValueError(
                f"Status inválido: {status}"
            )

        execucao = (
            self.execution_repository
            .atualizar_status(
                execution_id=execution_id,
                status=status,
                erro=erro,
            )
        )

        if execucao is None:
            raise ValueError(
                "Execução não encontrada."
            )

        return execucao

    def listar_por_competencia(
        self,
        competencia_id,
    ):

        return (
            self.execution_repository
            .listar_por_competencia(
                competencia_id
            )
        )
