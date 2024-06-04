"""empty message

Revision ID: a73aa45b397d
Revises: e26112b1ebcf
Create Date: 2023-09-24 23:07:03.502150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a73aa45b397d"
down_revision = "e26112b1ebcf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("new_comments")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "new_comments",
                sa.VARCHAR(length=128),
                autoincrement=False,
                nullable=True,
            )
        )

    # ### end Alembic commands ###