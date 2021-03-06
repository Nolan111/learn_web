"""Aded youtube_trailer_id to Film

Revision ID: 9a46f10c8a34
Revises: b3dc9df87547
Create Date: 2021-07-11 14:45:08.529159

"""
from os import name
from alembic import op
import sqlalchemy as sa
from youtub import get_video_id
from models import Film


# revision identifiers, used by Alembic.
revision = "b3dc9df87547"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("films", sa.Column("youtube_trailer_id", sa.String(length=25), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("films", "youtube_trailer_id")
    # ### end Alembic commands ###
