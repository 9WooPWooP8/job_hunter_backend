"""add status to resume

Revision ID: e0e992e4df8d
Revises: 2ab2aac6c475
Create Date: 2023-12-13 16:37:39.352129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.resumes.models import SearchStatus

# revision identifiers, used by Alembic.
revision: str = 'e0e992e4df8d'
down_revision: Union[str, None] = '2ab2aac6c475'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('search_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('search_statuses_pkey'))
    )
    op.drop_table('resume_personal_quality')
    op.drop_table('personal_qualities')
    op.add_column('resumes', sa.Column('personal_qualities', sa.String(), nullable=True))
    op.add_column('resumes', sa.Column('status_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('resumes_status_id_fkey'), 'resumes', 'search_statuses', ['status_id'], ['id'])
    # ### end Alembic commands ###

    op.bulk_insert(
        SearchStatus.__table__,
        [
            {'id': 1, 'status': 'В активном поиске'},
            {'id': 2, 'status': 'Трудоустроен'},
            {'id': 3, 'status': 'Не рассматривает предложения'}
        ]
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('resumes_status_id_fkey'), 'resumes', type_='foreignkey')
    op.drop_column('resumes', 'status_id')
    op.drop_column('resumes', 'personal_qualities')
    op.create_table('resume_personal_quality',
    sa.Column('resume_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('personal_quality_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['personal_quality_id'], ['personal_qualities.id'], name='resume_personal_quality_personal_quality_id_fkey'),
    sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], name='resume_personal_quality_resume_id_fkey'),
    sa.PrimaryKeyConstraint('resume_id', 'personal_quality_id', name='resume_personal_quality_pkey')
    )
    op.create_table('personal_qualities',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='personal_qualities_pkey')
    )
    op.drop_table('search_statuses')
    # ### end Alembic commands ###
