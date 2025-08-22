"""Adicionar tabela responsavel_tecnico_item

Revision ID: a1b2c3d4e5f6
Revises: f44eabf6633e
Create Date: 2025-08-18 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'f44eabf6633e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Verificar se a tabela responsavel_tecnico_item já existe
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Criar tabela de associação responsavel_tecnico_item se não existir
    if 'responsavel_tecnico_item' not in existing_tables:
        op.create_table('responsavel_tecnico_item',
        sa.Column('responsavel_tecnico_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['responsavel_tecnico_id'], ['users_safs.id'], name='fk_responsavel_tecnico_item_user_id'),
        sa.ForeignKeyConstraint(['item_id'], ['itens_catalogo.id'], name='fk_responsavel_tecnico_item_item_id'),
        sa.PrimaryKeyConstraint('responsavel_tecnico_id', 'item_id')
        )
    
    # Criar tabela de associação item_processo se não existir
    if 'item_processo' not in existing_tables:
        op.create_table('item_processo',
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('processo_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['itens_catalogo.id'], name='fk_item_processo_item_id'),
        sa.ForeignKeyConstraint(['processo_id'], ['planejamento_aquisicao.id'], name='fk_item_processo_processo_id'),
        sa.PrimaryKeyConstraint('item_id', 'processo_id')
        )


def downgrade() -> None:
    # Verificar se as tabelas existem antes de tentar removê-las
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names()
    
    # Remover tabelas se existirem
    if 'item_processo' in existing_tables:
        op.drop_table('item_processo')
    if 'responsavel_tecnico_item' in existing_tables:
        op.drop_table('responsavel_tecnico_item')