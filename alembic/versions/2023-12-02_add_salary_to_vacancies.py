"""add salary to vacancies

Revision ID: 83bfcf02369a
Revises: 89400c3c4127
Create Date: 2023-12-02 15:28:57.152444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "83bfcf02369a"
down_revision: Union[str, None] = "89400c3c4127"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("required_experiences")
    op.add_column(
        "vacancies", sa.Column("experience_min", sa.Integer(), nullable=False)
    )
    op.add_column(
        "vacancies", sa.Column("experience_max", sa.Integer(), nullable=False)
    )
    op.add_column("vacancies", sa.Column("salary_min", sa.Integer(), nullable=False))
    op.add_column("vacancies", sa.Column("salary_max", sa.Integer(), nullable=False))
    op.drop_constraint("vacancies_experience_id_fkey", "vacancies", type_="foreignkey")
    op.drop_column("vacancies", "experience_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "vacancies",
        sa.Column("experience_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key(
        "vacancies_experience_id_fkey",
        "vacancies",
        "required_experiences",
        ["experience_id"],
        ["id"],
    )
    op.drop_column("vacancies", "salary_max")
    op.drop_column("vacancies", "salary_min")
    op.drop_column("vacancies", "experience_max")
    op.drop_column("vacancies", "experience_min")
    op.create_table(
        "required_experiences",
        sa.Column(
            "id",
            sa.INTEGER(),
            sa.Identity(
                always=False,
                start=1,
                increment=1,
                minvalue=1,
                maxvalue=2147483647,
                cycle=False,
                cache=1,
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="required_experiences_pkey"),
    )
    # ### end Alembic commands ###
