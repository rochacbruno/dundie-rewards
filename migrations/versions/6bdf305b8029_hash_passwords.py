"""hash_passwords

Revision ID: 6bdf305b8029
Revises: c4abb08ab5d3
Create Date: 2024-08-09 15:50:41.755091

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from dundie.models import User
from dundie.utils.user import get_password_hash, verify_password
from sqlmodel import Session, select

# revision identifiers, used by Alembic.
revision = '6bdf305b8029'
down_revision = 'c4abb08ab5d3'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    users = session.exec(select(User).where(~User.password.like("$argon%")))

    for user in users:
        plain = user.password
        hashed = get_password_hash(plain)
        if verify_password(plain, hashed):
            user.password = hashed
            session.add(user)

    session.commit()


def downgrade():
    pass
