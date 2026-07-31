"""add_phase4_tables

Revision ID: c3d4e5f6a7b8
Revises: b2ac8182cf1a
Create Date: 2026-07-13 23:30:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2ac8182cf1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Extend AgentType enum with new values
    op.execute("ALTER TABLE agent_runs DROP CONSTRAINT IF EXISTS agenttype")
    op.execute("ALTER TABLE agent_runs ALTER COLUMN agent_type TYPE VARCHAR(50)")

    # Create processing_nodes table
    op.create_table('processing_nodes',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('parent_id', sa.String(), nullable=True),
    sa.Column('node_type', sa.Enum('chapter', 'topic', 'subtopic', name='nodetype'), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('metadata', sa.JSON(), nullable=True),
    sa.Column('chunk_ids', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['processing_nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_processing_nodes_document_id'), 'processing_nodes', ['document_id'], unique=False)
    op.create_index(op.f('ix_processing_nodes_parent_id'), 'processing_nodes', ['parent_id'], unique=False)

    # Create agent_outputs table
    op.create_table('agent_outputs',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('agent_type', sa.String(), nullable=False),
    sa.Column('params_hash', sa.String(), nullable=False),
    sa.Column('output_data', sa.JSON(), nullable=False),
    sa.Column('source_refs', sa.JSON(), nullable=True),
    sa.Column('token_usage', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document_id', 'agent_type', 'params_hash', name='uq_agent_output_cache')
    )
    op.create_index(op.f('ix_agent_outputs_document_id'), 'agent_outputs', ['document_id'], unique=False)

    # Create progress_events table
    op.create_table('progress_events',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=True),
    sa.Column('event_type', sa.Enum('quiz_completed', 'document_viewed', 'revision_studied', 'explanation_requested', 'recommendation_dismissed', name='eventtype'), nullable=False),
    sa.Column('event_data', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_progress_events_user_id'), 'progress_events', ['user_id'], unique=False)
    op.create_index(op.f('ix_progress_events_document_id'), 'progress_events', ['document_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_progress_events_document_id'), table_name='progress_events')
    op.drop_index(op.f('ix_progress_events_user_id'), table_name='progress_events')
    op.drop_table('progress_events')
    op.drop_index(op.f('ix_agent_outputs_document_id'), table_name='agent_outputs')
    op.drop_table('agent_outputs')
    op.drop_index(op.f('ix_processing_nodes_parent_id'), table_name='processing_nodes')
    op.drop_index(op.f('ix_processing_nodes_document_id'), table_name='processing_nodes')
    op.drop_table('processing_nodes')
