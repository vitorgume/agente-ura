from src.infrastructure.entity.mensagem_conversa_entity import MensagemConversaEntity
from src.domain.mensagem_conversa import MensagemConversa


class MensagemConversaMapper:

    def paraEntity(self, mensagem: MensagemConversa) -> MensagemConversaEntity:
        entidade = MensagemConversaEntity()
        entidade.id = mensagem.id
        entidade.responsavel = mensagem.responsavel
        entidade.conteudo = mensagem.conteudo
        entidade.conversa_id = mensagem.conversa_id
        entidade.data = mensagem.data
        return entidade
    
    def paraDomain(self, mensagemConversaEntity: MensagemConversaEntity) -> MensagemConversa:
        mensagemConversa = MensagemConversa(
            mensagemConversaEntity.id,
            mensagemConversaEntity.responsavel,
            mensagemConversaEntity.conteudo,
            mensagemConversaEntity.conversa_id,
            mensagemConversaEntity.data
        )
        return mensagemConversa
