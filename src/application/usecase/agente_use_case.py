from src.domain.conversa import Conversa
from src.infrastructure.dataprovider.agente_data_provider import AgenteDataProvider

class AgenteUseCase:

    def __init__(self, agente_data_provider: AgenteDataProvider):
        self.agente_data_provider = agente_data_provider

    def processar(self, mensagem: str, conversa: Conversa):
        return self.agente_data_provider.enviar_mensagem(mensagem, conversa.mensagens)
        