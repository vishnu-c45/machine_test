"""add course_id to students

Revision ID: b939b20f005b
Revises: 426807eb1818
Create Date: 2025-11-17 15:03:23.150770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b939b20f005b'
down_revision = '426807eb1818'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('students', sa.Column('course_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_students_course_id', 
        'students', 
        'courses', 
        ['course_id'], 
        ['id']
    )

def downgrade():
    op.drop_constraint('fk_students_course_id', 'students', type_='foreignkey')
    op.drop_column('students', 'course_id')
