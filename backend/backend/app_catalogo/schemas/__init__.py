# Pydantic Schemas
"""
Inicialização dos schemas com resolução de referências forward
"""

# Importar todos os schemas
from .user import User as UserRead
from .controle_processos import ProcessoRead
from .catalogo import ItemCatalogoRead

# Resolver referências forward
ProcessoRead.model_rebuild()
ItemCatalogoRead.model_rebuild()