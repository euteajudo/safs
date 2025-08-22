"""Remover completamente responsavel_tecnico - tabela e campo

Revision ID: zzz999999999
Revises: 092a11b55114
Create Date: 2025-08-21 19:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'zzz999999999'
down_revision: Union[str, None] = '092a11b55114'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remover tabela responsavel_tecnico_item e campo responsavel_tecnico"""
    
    # Verificar se a tabela existe antes de tentar remover
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    # Remover tabela responsavel_tecnico_item se existir
    if 'responsavel_tecnico_item' in existing_tables:
        op.drop_table('responsavel_tecnico_item')
    
    # Verificar se a coluna existe antes de tentar remover
    existing_columns = [col['name'] for col in inspector.get_columns('itens_catalogo')]
    
    # Remover coluna responsavel_tecnico da tabela itens_catalogo se existir
    if 'responsavel_tecnico' in existing_columns:
        op.drop_column('itens_catalogo', 'responsavel_tecnico')


def downgrade() -> None:
    """Restaurar tabela responsavel_tecnico_item e campo responsavel_tecnico"""
    
    # Restaurar coluna responsavel_tecnico na tabela itens_catalogo
    op.add_column('itens_catalogo', sa.Column('responsavel_tecnico', sa.String(100), nullable=True))
    
    # Restaurar tabela responsavel_tecnico_item
    op.create_table('responsavel_tecnico_item',
        sa.Column('responsavel_tecnico_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['responsavel_tecnico_id'], ['users_safs.id'], name='fk_responsavel_tecnico_item_user_id'),
        sa.ForeignKeyConstraint(['item_id'], ['itens_catalogo.id'], name='fk_responsavel_tecnico_item_item_id'),
        sa.PrimaryKeyConstraint('responsavel_tecnico_id', 'item_id')
    )