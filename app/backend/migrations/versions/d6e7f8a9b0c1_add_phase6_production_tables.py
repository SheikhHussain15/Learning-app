"""Add Phase 6 production infrastructure tables.

Revision ID: d6e7f8a9b0c1
Revises: c3d4e5f6a7b8
Create Date: 2026-07-16
"""
from alembic import op
import sqlalchemy as sa

revision = "d6e7f8a9b0c1"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "health_checks",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("component", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="healthy"),
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.String(500), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_health_checks_component", "health_checks", ["component"])

    op.create_table(
        "deployment_records",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("version", sa.String(20), nullable=False),
        sa.Column("environment", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("deployed_by", sa.String(255), nullable=False),
        sa.Column("deployed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rollback_from", sa.String(), nullable=True),
    )
    op.create_index("ix_deployment_records_environment", "deployment_records", ["environment"])

    op.create_table(
        "security_audit_logs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("event_type", sa.String(30), nullable=False),
        sa.Column("user_id", sa.String(255), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_security_audit_logs_event_type", "security_audit_logs", ["event_type"])
    op.create_index("ix_security_audit_logs_created_at", "security_audit_logs", ["created_at"])

    op.create_table(
        "test_suite_results",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("suite_type", sa.String(20), nullable=False),
        sa.Column("total_tests", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("passed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("skipped", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("coverage_percent", sa.Float(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("run_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("commit_sha", sa.String(40), nullable=True),
    )
    op.create_index("ix_test_suite_results_suite_type", "test_suite_results", ["suite_type"])
    op.create_index("ix_test_suite_results_run_at", "test_suite_results", ["run_at"])

    op.create_table(
        "secret_rotation_logs",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("secret_type", sa.String(20), nullable=False),
        sa.Column("rotated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("rotated_by", sa.String(255), nullable=False),
        sa.Column("previous_rotation", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_secret_rotation_logs_secret_type", "secret_rotation_logs", ["secret_type"])


def downgrade() -> None:
    op.drop_table("secret_rotation_logs")
    op.drop_table("test_suite_results")
    op.drop_table("security_audit_logs")
    op.drop_table("deployment_records")
    op.drop_table("health_checks")
