# coding=utf-8
"""add URL

Revision ID: 1770d17056aa
Revises: 24621aff524d
Create Date: 2017-05-05 09:35:34.426714

"""
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import Unicode, String

from clld.db.migration import Connection
from clld.db.models.common import Source, Sentence_files

# revision identifiers, used by Alembic.
revision = '1770d17056aa'
down_revision = '24621aff524d'

#1 | {"thumbnail": null, "web": null, "size": 179526, "objid": "EAEA0-9EEA-E2F2-6F6B-0", "original": "a.xlsx"}   | heathouattarahantgan2016lexicon-1                       | Heath_Ouattara_Hantgan_Tiefo-N_lexicon_spreadsheet.xlsx               |             |                    |   1 | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet       | 2016-10-25 12:35:26.65291+02 | t      | 2016-10-25 12:35:26.65291+02 |         1 |       1

def upgrade():
    conn = Connection(op.get_bind())

    spk = conn.pk()
    conn.insert()

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
