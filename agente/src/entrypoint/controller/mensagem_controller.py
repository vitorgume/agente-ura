from fastapi import FastAPI
from src.entrypoint.controller.dto.MensagemDto import MensagemDto
from src.application.usecase.mensagemUseCase import MensagemService

app = FastAPI()
service = MensagemService()

# Rota POST para receber mensagem e processar
@app.post("/chat")
def chat_endpoint(msg: MensagemDto):
    
    return {"resposta": resposta}
