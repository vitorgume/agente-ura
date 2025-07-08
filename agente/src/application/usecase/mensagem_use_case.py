from src.domain.mensagem import Mensagem
from src.application.usecase.conversa_use_case import ConversaUseCase

class MensagemUseCase:
    conversa_use_case: ConversaUseCase
    
    def __init__(self):
        pass

    def processar_mensagem(self, mensagem: Mensagem):
        conversa = conversa_use_case.consulta_por_id(mensagem.conversa_id)
        


        
        
        return "Resposta processada"