# coding=utf-8
"""add source file

Revision ID: 9320d2f7765b
Revises: 1770d17056aa
Create Date: 2017-05-05 09:58:20.128175

"""
from alembic import op

from clld.db.migration import Connection
from clld.db.models.common import Source, Source_files



# revision identifiers, used by Alembic.
revision = '9320d2f7765b'
down_revision = '1770d17056aa'


def upgrade():
    conn = Connection(op.get_bind())

    spk = conn.pk(Source, 'heathetal2015')
    conn.insert(
        Source_files,
        jsondata={
            "thumbnail": None,
            "web": None,
            "size": 7531008,
            "objid": "EAEA0-C97A-A1D2-2E76-0",
            "original": "a.xls"},
        id='heathetal2015-1',
        name='Dogon.comp.vocab.UNICODE.xls',
        ord=1,
        mime_type='application/vnd.ms-excel',
        object_pk=spk)


def downgrade():
    pass
