from src.infrastructure.entity.conversa_entity import ConversaEntity
from src.infrastructure.mapper.mensagem_conversa_mapper import MensagemConversaMapper
from src.domain.conversa import Conversa


class ConversaMapper:

    def __init__(self, mensagem_conversa_mapper: MensagemConversaMapper):
        self.mensagem_conversa_mapper = mensagem_conversa_mapper

    def paraEntity(self, conversa: Conversa) -> ConversaEntity:
        return ConversaEntity(
            id=conversa.id,
            cliente_id=conversa.cliente_id,
            mensagens=[self.mensagem_conversa_mapper.paraEntity(m) for m in conversa.mensagens]
        )

    def paraDomain(self, conversa_entity: ConversaEntity) -> Conversa:
        return Conversa(
            id=conversa_entity.id,
            cliente_id=conversa_entity.cliente_id,
            mensagens=[self.mensagem_conversa_mapper.paraDomain(m) for m in conversa_entity.mensagens]
        )
