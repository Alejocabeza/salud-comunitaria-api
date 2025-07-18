"""create_resource_table

Revision ID: 694f879b4e61
Revises: 5a5231b1c3d5
Create Date: 2025-07-12 10:05:10.867653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '694f879b4e61'
down_revision: Union[str, None] = '5a5231b1c3d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('dose', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('in_stock', sa.Boolean(), nullable=True),
    sa.Column('outpatient_center_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('updated_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('deleted_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['outpatient_center_id'], ['outpatient_centers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('auths_roles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_auths_roles_role_id'))
        batch_op.drop_index(batch_op.f('ix_auths_roles_user_id'))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'roles', ['role_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'auths', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('roles_permissions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_roles_permissions_permission_id'))
        batch_op.drop_index(batch_op.f('ix_roles_permissions_role_id'))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'roles', ['role_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'permissions', ['permission_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('users_permissions', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_permissions_permission_id'))
        batch_op.drop_index(batch_op.f('ix_users_permissions_user_id'))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'auths', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'permissions', ['permission_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_permissions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'permissions', ['permission_id'], ['id'])
        batch_op.create_foreign_key(None, 'auths', ['user_id'], ['id'])
        batch_op.create_index(batch_op.f('ix_users_permissions_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_permissions_permission_id'), ['permission_id'], unique=False)

    with op.batch_alter_table('roles_permissions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'permissions', ['permission_id'], ['id'])
        batch_op.create_foreign_key(None, 'roles', ['role_id'], ['id'])
        batch_op.create_index(batch_op.f('ix_roles_permissions_role_id'), ['role_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_roles_permissions_permission_id'), ['permission_id'], unique=False)

    with op.batch_alter_table('auths_roles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'roles', ['role_id'], ['id'])
        batch_op.create_foreign_key(None, 'auths', ['user_id'], ['id'])
        batch_op.create_index(batch_op.f('ix_auths_roles_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_auths_roles_role_id'), ['role_id'], unique=False)

    op.drop_table('resources')
    # ### end Alembic commands ###
