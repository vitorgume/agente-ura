from src.application.usecase import conversa_use_case
from src.application.usecase.conversa_use_case import ConversaUseCase
from src.domain.conversa import Conversa
from src.infrastructure.dataprovider.agente_data_provider import AgenteDataProvider

class AgenteUseCase:

    agente_data_provider: AgenteDataProvider
    conversa_use_case: ConversaUseCase

    def processar(mensagem: str, conversa: Conversa):
        return agente_data_provider.enviar_mensagem(mensagem, conversa.mensagens)
        