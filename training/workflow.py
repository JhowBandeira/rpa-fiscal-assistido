from dataclasses import dataclass, field

@dataclass
class TrainingRequest:
    routine_key: str
    routine_name: str
    status: str = "AGUARDANDO_TREINAMENTO"
    requested_inputs: list[str] = field(default_factory=lambda: [
        "Print da tela inicial",
        "Caminho/menu utilizado",
        "Print da próxima tela",
        "Campos preenchidos",
        "Botões acionados",
        "Resultado esperado",
        "Forma/local de salvamento, quando houver",
    ])
