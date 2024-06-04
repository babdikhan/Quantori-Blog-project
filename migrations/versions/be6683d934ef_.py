"""empty message

Revision ID: be6683d934ef
Revises: a73aa45b397d
Create Date: 2023-09-26 00:38:30.895230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "be6683d934ef"
down_revision = "a73aa45b397d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_favorite",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_favorite")
    # ### end Alembic commands ###
