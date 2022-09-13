"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


<<<<<<< HEAD
def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
=======
def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
>>>>>>> projeto-dundie-rewards/main
    ${downgrades if downgrades else "pass"}
