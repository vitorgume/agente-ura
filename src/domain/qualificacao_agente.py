from dataclasses import dataclass

@dataclass
class QualificacaoAgente:
    qualificado: bool
    nome: str
    segmento: int
    regiao: int
    descricao_material: str