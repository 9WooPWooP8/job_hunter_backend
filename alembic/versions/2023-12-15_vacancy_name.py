"""vacancy name

Revision ID: 3e1e9bdee16c
Revises: 8c3f27ee292d
Create Date: 2023-12-15 05:13:26.738819

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3e1e9bdee16c"
down_revision: Union[str, None] = "8c3f27ee292d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "vacancies", sa.Column("name", sa.String(), nullable=False, server_default="")
    )
    op.alter_column("vacancies", "name", server_default=None)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("vacancies", "name")
    # ### end Alembic commands ###
