from dataclasses import dataclass
from src.domain.mensagem import Mensagem
from src.application.usecase.conversa_use_case import ConversaUseCase
from src.application.usecase.agente_use_case import AgenteUseCase

class MensagemUseCase:
    
    def __init__(self, conversa_use_case: ConversaUseCase, agente_use_case: AgenteUseCase):
        self.conversa_use_case = conversa_use_case
        self.agente_use_case = agente_use_case

    def processar_mensagem(self, mensagem: Mensagem):
        conversa = self.conversa_use_case.consulta_por_id(mensagem.conversa_id)
        respostaAgente = self.agente_use_case.processar(mensagem.message, conversa)
        
        mensagem_resposta = MensagemConversa(
            id=str(uuid.uuid4()),
            responsavel="agente",
            conteudo=respostaAgente,
            conversa_id=conversa.id
        )
        
        conversa.mensagens.append(mensagem_resposta)
        self.conversa_use_case.atualiza(conversa)

        return respostaAgente