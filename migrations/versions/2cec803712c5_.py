"""empty message

Revision ID: 2cec803712c5
Revises: 
Create Date: 2021-11-10 01:06:57.078540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cec803712c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products_type',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('type_id')
    )
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(length=50), nullable=False),
    sa.Column('service_desc', sa.String(length=150), nullable=True),
    sa.Column('service_icon', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=False),
    sa.Column('user_lname', sa.String(length=50), nullable=False),
    sa.Column('user_email', sa.String(length=100), nullable=False),
    sa.Column('user_password', sa.String(length=100), nullable=False),
    sa.Column('user_role', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_email')
    )
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=50), nullable=False),
    sa.Column('product_desc', sa.String(length=150), nullable=True),
    sa.Column('product_brand', sa.String(length=100), nullable=True),
    sa.Column('product_price', sa.Integer(), nullable=False),
    sa.Column('product_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_type_id'], ['products_type.type_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('shopping_card',
    sa.Column('shop_id', sa.Integer(), nullable=False),
    sa.Column('shop_user_id', sa.Integer(), nullable=False),
    sa.Column('shop_product_id', sa.Integer(), nullable=False),
    sa.Column('shop_service_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shop_product_id'], ['products.product_id'], ),
    sa.ForeignKeyConstraint(['shop_service_id'], ['services.service_id'], ),
    sa.ForeignKeyConstraint(['shop_user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('shop_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shopping_card')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('services')
    op.drop_table('products_type')
    # ### end Alembic commands ###
