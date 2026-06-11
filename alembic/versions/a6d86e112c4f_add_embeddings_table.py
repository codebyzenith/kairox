from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision: str = 'a6d86e112c4f'
down_revision: Union[str, None] = '3e1f6ce82241'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('embeddings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('article_id', sa.UUID(), nullable=True),
        sa.Column('embedding', Vector(384), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('article_id')
    )

def downgrade() -> None:
    op.drop_table('embeddings')