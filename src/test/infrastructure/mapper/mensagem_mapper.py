import uuid
import datetime
import pytest
from unittest.mock import Mock

from src.infrastructure.mapper.conversa_mapper import ConversaMapper
from src.domain.conversa import Conversa
from src.infrastructure.entity.conversa_entity import ConversaEntity, MensagemConversaEntity
from src.infrastructure.mapper.mensagem_conversa_mapper import MensagemConversaMapper

@pytest.fixture
def mensagem_mapper_mock():
    mock = Mock(spec=MensagemConversaMapper)

    # Dummy entity para tests
    dummy_entity = MensagemConversaEntity()
    dummy_entity.id_mensagem   = uuid.uuid4().bytes
    dummy_entity.conversa_id   = uuid.UUID("00000000-0000-0000-0000-000000000000").bytes
    dummy_entity.conteudo      = "irrelevante"
    dummy_entity.timestamp     = datetime.datetime(2025, 7, 25, 12, 0, 0)

    mock.paraEntity.return_value = dummy_entity
    mock.paraDomain.return_value = "MSG_DOMAIN"
    return mock

@pytest.fixture
def conversa_mapper(mensagem_mapper_mock):
    return ConversaMapper(mensagem_conversa_mapper=mensagem_mapper_mock)

def make_conversa():
    cid = str(uuid.uuid4())
    return Conversa(
        id=str(uuid.uuid4()),
        data_criacao=datetime.datetime(2025,7,25,12,0,0),
        finalizada=False,
        inativa=False,
        cliente_id_cliente=cid,
        vendedor_id_vendedor="123",
        cliente_id=cid,
        mensagens=["msg1","msg2"]
    )

def test_para_entity(mensagem_mapper_mock, conversa_mapper):
    # given
    conversa = make_conversa()

    # when
    entity: ConversaEntity = conversa_mapper.paraEntity(conversa)

    # then: mapeamento dos campos básicos
    assert entity.id_conversa == uuid.UUID(conversa.id).bytes
    assert entity.data_criacao == conversa.data_criacao
    assert entity.finalizada == conversa.finalizada
    assert entity.inativa == conversa.inativa

    # then: chaves estrangeiras
    assert entity.cliente_id_cliente == uuid.UUID(conversa.cliente_id_cliente).bytes
    assert entity.vendedor_id_vendedor == int(conversa.vendedor_id_vendedor)

    # then: mensagens
    # o mock deve ter sido chamado uma vez para cada mensagem
    assert mensagem_mapper_mock.paraEntity.call_count == len(conversa.mensagens)
    # e a lista de entity.mensagens deve conter sempre o dummy_entity
    assert all(isinstance(m, MensagemConversaEntity) for m in entity.mensagens)

def test_para_domain(mensagem_mapper_mock, conversa_mapper):
    # given
    conversa = make_conversa()

    # criar dummy_msg para montar a ConversationEntity manualmente
    dummy_msg = MensagemConversaEntity()
    dummy_msg.id_mensagem   = uuid.uuid4().bytes
    dummy_msg.conversa_id   = uuid.UUID(conversa.id).bytes
    dummy_msg.conteudo      = "irrelevante"
    dummy_msg.timestamp     = conversa.data_criacao

    entity = ConversaEntity(
        id_conversa=uuid.UUID(conversa.id).bytes,
        data_criacao=conversa.data_criacao,
        finalizada=conversa.finalizada,
        inativa=conversa.inativa,
        cliente_id_cliente=uuid.UUID(conversa.cliente_id_cliente).bytes,
        vendedor_id_vendedor=int(conversa.vendedor_id_vendedor),
        mensagens=[dummy_msg, dummy_msg]
    )

    # when
    domain: Conversa = conversa_mapper.paraDomain(entity)

    # then: campos básicos de volta
    assert domain.id == conversa.id
    assert domain.data_criacao == conversa.data_criacao.isoformat()
    assert domain.finalizada == conversa.finalizada
    assert domain.inativa == conversa.inativa

    # then: ids voltam como string
    assert domain.cliente_id_cliente == conversa.cliente_id_cliente
    assert domain.vendedor_id_vendedor == conversa.vendedor_id_vendedor
    assert domain.cliente_id == conversa.cliente_id

    # then: mensagens de volta
    assert mensagem_mapper_mock.paraDomain.call_count == len(entity.mensagens)
    assert domain.mensagens == ["MSG_DOMAIN", "MSG_DOMAIN"]
