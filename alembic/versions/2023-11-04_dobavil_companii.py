"""dobavil companii

Revision ID: d8dbdb75a214
Revises: 6760ca0f66e0
Create Date: 2023-11-04 14:08:24.319031

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d8dbdb75a214"
down_revision: Union[str, None] = "6760ca0f66e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["recruiters.user_id"], name=op.f("companies_owner_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("companies_pkey")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("companies")
    # ### end Alembic commands ###
