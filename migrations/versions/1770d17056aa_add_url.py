# coding=utf-8
"""add URL

Revision ID: 1770d17056aa
Revises: 24621aff524d
Create Date: 2017-05-05 09:35:34.426714

"""
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import Unicode, String

# revision identifiers, used by Alembic.
revision = '1770d17056aa'
down_revision = '24621aff524d'


def upgrade():
    source = table(
        'source', column('id', String), column('url', Unicode), column('note', Unicode))
    op.execute(
        source.update()
        .where(source.c.id == op.inline_literal('heathetal2015'))
        .values({
            'url': op.inline_literal(
                'http://cdstar.shh.mpg.de/bitstreams/EAEA0-C97A-A1D2-2E76-0/a.xls'),
            'note': op.inline_literal('')})
    )


def downgrade():
    pass
