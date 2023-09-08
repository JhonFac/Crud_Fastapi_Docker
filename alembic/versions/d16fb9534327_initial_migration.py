"""Initial migration

Revision ID: d16fb9534327
Revises: 
Create Date: 2023-09-07 12:33:36.261271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd16fb9534327'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('cel_number', sa.String(), nullable=True),
    sa.Column('dress', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_people_cel_number'), 'people', ['cel_number'], unique=False)
    op.create_index(op.f('ix_people_city'), 'people', ['city'], unique=False)
    op.create_index(op.f('ix_people_dress'), 'people', ['dress'], unique=False)
    op.create_index(op.f('ix_people_first_name'), 'people', ['first_name'], unique=False)
    op.create_index(op.f('ix_people_id'), 'people', ['id'], unique=False)
    op.create_index(op.f('ix_people_last_name'), 'people', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_people_last_name'), table_name='people')
    op.drop_index(op.f('ix_people_id'), table_name='people')
    op.drop_index(op.f('ix_people_first_name'), table_name='people')
    op.drop_index(op.f('ix_people_dress'), table_name='people')
    op.drop_index(op.f('ix_people_city'), table_name='people')
    op.drop_index(op.f('ix_people_cel_number'), table_name='people')
    op.drop_table('people')
    # ### end Alembic commands ###
