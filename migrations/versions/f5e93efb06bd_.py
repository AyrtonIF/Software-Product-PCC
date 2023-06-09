"""empty message

Revision ID: f5e93efb06bd
Revises: 
Create Date: 2023-04-04 17:39:31.761205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5e93efb06bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Produtos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_produto', sa.String(), nullable=True),
    sa.Column('codigo_produto', sa.Integer(), nullable=True),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.Column('produto', sa.String(), nullable=True),
    sa.Column('data_cadastro', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('codigo_produto')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Produtos')
    # ### end Alembic commands ###
