from src.domain.mensagem import Mensagem
from src.application.usecase.conversa_use_case import ConversaUseCase
from src.application.usecase.agente_use_case import AgenteUseCase

class MensagemUseCase:
    conversa_use_case: ConversaUseCase
    agente_use_case: AgenteUseCase
    
    def __init__(self):
        pass

    def processar_mensagem(self, mensagem: Mensagem):
        conversa = conversa_use_case.consulta_por_id(mensagem.conversa_id)
        respostaAgente = agente_use_case.processar(mensagem.message, conversa)
        
        mensagem_resposta = MensagemConversa(
            id=str(uuid.uuid4()),
            responsavel="agente",
            conteudo=respostaAgente,
            conversa_id=conversa.id
        )
        
        conversa.mensagens.append(mensagem_resposta)
        conversa_use_case.atualiza(conversa)
        return respostaAgente