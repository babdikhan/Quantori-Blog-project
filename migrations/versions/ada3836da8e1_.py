"""empty message

Revision ID: ada3836da8e1
Revises: b28c5f45b535
Create Date: 2023-08-31 10:54:55.768254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ada3836da8e1"
down_revision = "b28c5f45b535"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("new_comments", sa.String(length=128), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("new_comments")

    # ### end Alembic commands ###
