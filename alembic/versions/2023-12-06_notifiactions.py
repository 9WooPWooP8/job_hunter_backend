"""notifiactions

Revision ID: f1b2905b82c1
Revises: 2ec6c74145bb
Create Date: 2023-12-06 09:04:10.437915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1b2905b82c1"
down_revision: Union[str, None] = "2ec6c74145bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("applicant_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["applicant_id"],
            ["applicants.user_id"],
            name=op.f("notifications_applicant_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", "applicant_id", name=op.f("notifications_pkey")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notifications")
    # ### end Alembic commands ###
