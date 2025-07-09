class ConversaNaoEncontradaException:
    def __init__(self):
        super().__init__(f"Conversa não encontrada pelo seu id.")