from src.domain.mensagem_conversa import MensagemConversa
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Conversa:
    id: str
    cliente_id: str
    mensagens: List[MensagemConversa]
    data_criacao: Optional[str]
    finalizada: bool
    cliente_id_cliente: Optional[str]
    vendedor_id_vendedor: Optional[str]
