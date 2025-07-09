from fastapi import FastAPI
from src.entrypoint.controller.dto.mensagem_dto import MensagemDto
from src.application.usecase.mensagem_use_case import MensagemUseCase
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


app = FastAPI()
service = MensagemUseCase()

# Rota POST para receber mensagem e processar
@app.post("/chat")
def chat_endpoint(msg: MensagemDto):
    service.processar_mensagem(msg)
    return {"resposta": resposta}
