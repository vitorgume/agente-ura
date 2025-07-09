from src.domain.conversa import Conversa
from src.infrastructure.dataprovider.conversa_data_provider import ConversaDataProvider

class ConversaUseCase:
    
    conversa_data_provider: ConversaDataProvider
    
    def consulta_por_id(self, id: str) -> Conversa:
        conversa = conversa_data_provider.consultar_por_id(id)
        if conversa is None:
            raise ConversaNaoEncontradaException()
        return conversa
    
    def atualiza(conversa: Conversa):
        conversa_data_provider.salvar(conversa)
        