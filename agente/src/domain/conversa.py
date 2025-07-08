from src.domain.mensagem_conversa import MensagemConversa

class Conversa: 
    id: str
    user_id: str
    mensagens: list[MensagemConversa]