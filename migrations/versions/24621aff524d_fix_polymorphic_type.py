# coding=utf-8
"""fix polymorphic_type

Revision ID: 24621aff524d
Revises: None
Create Date: 2014-11-26 14:35:53.101000

"""

# revision identifiers, used by Alembic.
revision = '24621aff524d'
down_revision = None

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['parameter', 'value'], 'base', 'custom')


def downgrade():
    update_pmtype(['parameter', 'value'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
