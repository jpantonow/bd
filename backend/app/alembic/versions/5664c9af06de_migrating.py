"""migrating

Revision ID: 5664c9af06de
Revises: b05af6a7aaba
Create Date: 2024-09-04 10:14:06.684611

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5664c9af06de'
down_revision = 'b05af6a7aaba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refeicao',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('calorias', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dieta',
    sa.Column('id_ref_manha', sa.Integer(), nullable=True),
    sa.Column('id_ref_tarde', sa.Integer(), nullable=True),
    sa.Column('id_ref_noite', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ref_manha'], ['refeicao.id'], ),
    sa.ForeignKeyConstraint(['id_ref_noite'], ['refeicao.id'], ),
    sa.ForeignKeyConstraint(['id_ref_tarde'], ['refeicao.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dieta')
    op.drop_table('refeicao')
    # ### end Alembic commands ###
