# Importações explícitas de todos os modelos para garantir que sejam registrados no metadata
from .base import Base
from .user import User
from .catalogo import ItensCatalogo
from .controle_processo import PlanejamentoAquisicao

# Disponibilizar os modelos para importação
__all__ = ['Base', 'User', 'ItensCatalogo', 'PlanejamentoAquisicao'] 