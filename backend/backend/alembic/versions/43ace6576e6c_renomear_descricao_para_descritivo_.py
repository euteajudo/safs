"""renomear_descricao_para_descritivo_resumido

Revision ID: 43ace6576e6c
Revises: af99e506b899
Create Date: 2025-08-20 14:30:55.910559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43ace6576e6c'
down_revision: Union[str, None] = 'af99e506b899'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Renomear coluna descricao para descritivo_resumido
    op.alter_column('itens_catalogo', 'descricao', 
                    new_column_name='descritivo_resumido',
                    type_=sa.String(300))  # Aumentar tamanho conforme modelo
    
    # Adicionar coluna descritivo_detalhado
    op.add_column('itens_catalogo', sa.Column('descritivo_detalhado', sa.String(4000), nullable=True))
    
    # Adicionar coluna responsavel_tecnico
    op.add_column('itens_catalogo', sa.Column('responsavel_tecnico', sa.String(100), nullable=True))


def downgrade() -> None:
    # Reverter alterações
    op.drop_column('itens_catalogo', 'responsavel_tecnico')
    op.drop_column('itens_catalogo', 'descritivo_detalhado')
    op.alter_column('itens_catalogo', 'descritivo_resumido', 
                    new_column_name='descricao',
                    type_=sa.String(255))
