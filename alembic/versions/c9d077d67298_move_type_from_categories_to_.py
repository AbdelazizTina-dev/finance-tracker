"""move type from categories to transactions

Revision ID: c9d077d67298
Revises: d3cce27df222
Create Date: 2026-10-02 21:26:19.998704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9d077d67298'
down_revision: Union[str, Sequence[str], None] = 'd3cce27df222'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""    
    conn = op.get_bind()
    orphans = conn.execute(
        sa.text("SELECT count(*) FROM transactions WHERE category_id IS NULL")
    ).scalar()
    if orphans:
        raise RuntimeError(
            f"{orphans} transactions have no category, so their type can't be "
            "backfilled. Assign them a category first, then rerun."
        )
    
    op.add_column('transactions', sa.Column('type', sa.String(length=10), nullable=True))
    op.execute('''
        UPDATE transactions AS t
        SET type = c.type
        FROM categories AS c
        WHERE t.category_id = c.id;
    ''')
    op.alter_column('transactions', 'type', nullable=False)
    op.create_check_constraint('transactions_type_check', 'transactions', "type IN ('income', 'expense')")
    op.drop_column('categories', 'type')


def downgrade() -> None:
    raise NotImplementedError(
        "Cannot automatically restore category types after moving them to transactions."
    )
