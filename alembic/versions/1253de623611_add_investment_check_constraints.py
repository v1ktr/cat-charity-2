"""Add investment check constraints

Revision ID: 1253de623611
Revises: 5580c6f4367e
Create Date: 2026-11-08 18:57:24.966566

"""
from alembic import op


revision = '1253de623611'
down_revision = '5580c6f4367e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('charityproject') as batch_op:
        batch_op.create_check_constraint(
            'ck_charityproject_full_amount_positive',
            'full_amount > 0',
        )
        batch_op.create_check_constraint(
            'ck_charityproject_invested_le_full_amount',
            'invested_amount <= full_amount',
        )
    with op.batch_alter_table('donation') as batch_op:
        batch_op.create_check_constraint(
            'ck_donation_full_amount_positive',
            'full_amount > 0',
        )
        batch_op.create_check_constraint(
            'ck_donation_invested_le_full_amount',
            'invested_amount <= full_amount',
        )


def downgrade():
    with op.batch_alter_table('donation') as batch_op:
        batch_op.drop_constraint(
            'ck_donation_invested_le_full_amount',
            type_='check',
        )
        batch_op.drop_constraint(
            'ck_donation_full_amount_positive',
            type_='check',
        )
    with op.batch_alter_table('charityproject') as batch_op:
        batch_op.drop_constraint(
            'ck_charityproject_invested_le_full_amount',
            type_='check',
        )
        batch_op.drop_constraint(
            'ck_charityproject_full_amount_positive',
            type_='check',
        )
