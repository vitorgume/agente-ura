from fastapi import FastAPI
from src.infrastructure.mapper.conversa_mapper import ConversaMapper
from src.infrastructure.mapper.mensagem_conversa_mapper import MensagemConversaMapper
from src.entrypoint.controller.mapper.mensagem_mapper import MensagemMapper
from src.entrypoint.controller.dto.mensagem_dto import MensagemDto
from src.application.usecase.mensagem_use_case import MensagemUseCase
from src.application.usecase.agente_use_case import AgenteUseCase
from src.application.usecase.conversa_use_case import ConversaUseCase
from src.infrastructure.dataprovider.conversa_data_provider import ConversaDataProvider
from src.infrastructure.dataprovider.agente_data_provider import AgenteDataProvider

import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI()

mensagem_conversa_mapper = MensagemConversaMapper()
conversa_mapper = ConversaMapper(mensagem_conversa_mapper)

mensagem_mapper = MensagemMapper()
conversa_data_provider = ConversaDataProvider(conversa_mapper)
agente_data_provider = AgenteDataProvider()

conversa_use_case = ConversaUseCase(conversa_data_provider)
agente_use_case = AgenteUseCase(agente_data_provider)

mensagem_use_case = MensagemUseCase(
    conversa_use_case=conversa_use_case,
    agente_use_case=agente_use_case
)

@app.post("/chat")
def chat_endpoint(msg: MensagemDto):
    mensagem_domain = mensagem_mapper.paraDomain(msg)
    resposta = mensagem_use_case.processar_mensagem(mensagem_domain)
    return resposta
