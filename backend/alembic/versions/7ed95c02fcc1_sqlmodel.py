"""SQLModel

Revision ID: 7ed95c02fcc1
Revises: 5055fc3e627c
Create Date: 2021-09-01 10:04:28.897386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "7ed95c02fcc1"
down_revision = "5055fc3e627c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Rename Tables
    op.rename_table("games", "game")
    op.rename_table("players", "player")
    op.rename_table("servers", "server")
    op.rename_table("channels", "channel")
    op.rename_table("members", "member")
    op.rename_table("o_auth2_token", "oauth2token")
    op.rename_table("parties", "party")
    op.rename_table("roles", "role")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # Rename tables
    op.rename_table("game", "games")
    op.rename_table("player", "players")
    op.rename_table("server", "servers")
    op.rename_table("channel", "channels")
    op.rename_table("member", "members")
    op.rename_table("oauth2token", "o_auth2_token")
    op.rename_table("party", "parties")
    op.rename_table("role", "roles")
    # ### end Alembic commands ###
