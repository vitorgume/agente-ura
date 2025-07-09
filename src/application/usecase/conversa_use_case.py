from src.domain.conversa import Conversa
from src.infrastructure.dataprovider.conversa_data_provider import ConversaDataProvider

class ConversaUseCase:
    
    def __init__(self, conversa_data_provider: ConversaDataProvider):
        self.conversa_data_provider = conversa_data_provider
    
    def consulta_por_id(self, id: str) -> Conversa:
        conversa = self.conversa_data_provider.consulta_por_id(id)
        if conversa is None:
            raise ConversaNaoEncontradaException()
        return conversa
    
    def atualiza(self, conversa: Conversa):
        self.conversa_data_provider.salvar(conversa)
        