"""
API Routers Package

Contém todos os roteadores da API:
- login: Autenticação e autorização
- users: Gerenciamento de usuários  
- catalogo: Catálogo de itens
- controle_processos: Processos de aquisição
- resp_tec: Responsáveis técnicos
"""

# Facilita importações futuras
from . import login
from . import users  
from . import catalogo
from . import controle_processos
from . import resp_tec

__all__ = ['login', 'users', 'catalogo', 'controle_processos', 'resp_tec'] 