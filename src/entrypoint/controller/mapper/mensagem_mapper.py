from domain.mensagem import Mensagem
from entrypoint.controller.dto.mensagem_dto import MensagemDto


class MensagemMapper:
    
    def paraDomain(dto: MensagemDto) -> Mensagem:
        return Mensagem(
            user_id=dto.user_id,
            message=dto.message
        )
        
    def paraDto(domain: Mensagem) -> MensagemDto:
        return MensagemDto(
            user_id=domain.user_id,
            message=domain.message
        )