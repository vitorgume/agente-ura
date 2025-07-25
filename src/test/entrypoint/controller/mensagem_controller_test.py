import pytest
from fastapi.testclient import TestClient

import src.entrypoint.controller.mensagem_controller as app_module

@pytest.fixture(autouse=True)
def client(monkeypatch):
    monkeypatch.setattr(
        app_module.mensagem_use_case,
        "processar_mensagem",
        lambda mensagem_domain: {"reply": f"Echo: {mensagem_domain.message}"}
    )

    monkeypatch.setattr(
        app_module.json_use_case,
        "transformar",
        lambda s: {"json": s.upper()}
    )

    return TestClient(app_module.app)

def test_chat_endpoint_success(client):
    payload = {
        "cliente_id": "cliente-123",
        "conversa_id": "conv-456",
        "message": "Olá, mundo!"
    }

    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert response.json() == {"reply": "Echo: Olá, mundo!"}

def test_chat_endpoint_missing_field(client):
    payload = {
        "cliente_id": "cliente-123",
        "conversa_id": "conv-456"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 422

def test_chat_json_endpoint_success(client):
    payload = {"mensagem": "testando json"}
    response = client.post("/chat/json", json=payload)
    assert response.status_code == 200
    assert response.json() == {"json": "TESTANDO JSON"}

def test_chat_json_endpoint_invalid_body(client):
    response = client.post("/chat/json", json={"msg": "oi"})
    assert response.status_code == 422
