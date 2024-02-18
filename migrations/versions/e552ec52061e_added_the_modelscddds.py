"""Added the modelscddds

Revision ID: e552ec52061e
Revises: e0201152b48b
Create Date: 2024-02-18 01:35:23.154544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e552ec52061e'
down_revision = 'e0201152b48b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('date_of_birth', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('contact_number', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(length=250), nullable=True))
        batch_op.drop_column('DateOfBirth')
        batch_op.drop_column('LastName')
        batch_op.drop_column('Description')
        batch_op.drop_column('ContactNumber')
        batch_op.drop_column('Gender')
        batch_op.drop_column('FirstName')
        batch_op.drop_column('Address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Address', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('FirstName', sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('Gender', sa.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('ContactNumber', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('Description', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('LastName', sa.VARCHAR(length=20), nullable=False))
        batch_op.add_column(sa.Column('DateOfBirth', sa.DATETIME(), nullable=True))
        batch_op.drop_column('description')
        batch_op.drop_column('address')
        batch_op.drop_column('contact_number')
        batch_op.drop_column('gender')
        batch_op.drop_column('date_of_birth')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###