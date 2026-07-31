"""add_phase5_learning_experience_tables

Revision ID: e7f8a9b0c1d2
Revises: c3d4e5f6a7b8
Create Date: 2026-07-18 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'e7f8a9b0c1d2'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create workspace_sections table
    op.create_table('workspace_sections',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('section_type', sa.Enum('summary', 'explanation', 'translation', 'diagram', 'quiz', 'flashcard', 'revision_notes', name='sectiontype'), nullable=False),
    sa.Column('status', sa.Enum('not_requested', 'processing', 'failed', 'completed', name='sectionstatus'), nullable=False),
    sa.Column('content', sa.JSON(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('requested_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workspace_sections_document_id'), 'workspace_sections', ['document_id'], unique=False)

    # Create quiz_attempts table
    op.create_table('quiz_attempts',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('quiz_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('total_questions', sa.Integer(), nullable=False),
    sa.Column('correct_answers', sa.Integer(), nullable=True),
    sa.Column('answers', sa.JSON(), nullable=True),
    sa.Column('time_spent', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('in_progress', 'completed', 'abandoned', name='quizattemptstatus'), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_attempts_quiz_id'), 'quiz_attempts', ['quiz_id'], unique=False)
    op.create_index(op.f('ix_quiz_attempts_user_id'), 'quiz_attempts', ['user_id'], unique=False)

    # Create flashcard_reviews table
    op.create_table('flashcard_reviews',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('flashcard_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('difficulty_rating', sa.Enum('easy', 'medium', 'hard', name='difficultyrating'), nullable=False),
    sa.Column('review_duration', sa.Integer(), nullable=True),
    sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('next_review_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('review_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flashcard_reviews_flashcard_id'), 'flashcard_reviews', ['flashcard_id'], unique=False)
    op.create_index(op.f('ix_flashcard_reviews_user_id'), 'flashcard_reviews', ['user_id'], unique=False)

    # Create tutor_conversations table
    op.create_table('tutor_conversations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('messages', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tutor_conversations_document_id'), 'tutor_conversations', ['document_id'], unique=False)
    op.create_index(op.f('ix_tutor_conversations_user_id'), 'tutor_conversations', ['user_id'], unique=False)

    # Create recommendations table
    op.create_table('recommendations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('recommendation_type', sa.Enum('document', 'quiz', 'flashcard', 'review', name='recommendationtype'), nullable=False),
    sa.Column('document_id', sa.String(), nullable=True),
    sa.Column('section_id', sa.String(), nullable=True),
    sa.Column('reason', sa.String(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recommendations_user_id'), 'recommendations', ['user_id'], unique=False)

    # Create user_notes table
    op.create_table('user_notes',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('section_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_notes_user_id'), 'user_notes', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_notes_document_id'), 'user_notes', ['document_id'], unique=False)

    # Add missing columns to progress_events table
    op.add_column('progress_events', sa.Column('section_id', sa.String(), nullable=True))
    op.add_column('progress_events', sa.Column('duration', sa.Integer(), nullable=True))

    # Update progress_events event_type enum to match model definition
    op.execute("ALTER TABLE progress_events DROP CONSTRAINT IF EXISTS eventtype")
    op.execute("ALTER TABLE progress_events ALTER COLUMN event_type TYPE VARCHAR(50)")


def downgrade() -> None:
    op.drop_column('progress_events', 'duration')
    op.drop_column('progress_events', 'section_id')

    op.drop_index(op.f('ix_user_notes_document_id'), table_name='user_notes')
    op.drop_index(op.f('ix_user_notes_user_id'), table_name='user_notes')
    op.drop_table('user_notes')

    op.drop_index(op.f('ix_recommendations_user_id'), table_name='recommendations')
    op.drop_table('recommendations')

    op.drop_index(op.f('ix_tutor_conversations_user_id'), table_name='tutor_conversations')
    op.drop_index(op.f('ix_tutor_conversations_document_id'), table_name='tutor_conversations')
    op.drop_table('tutor_conversations')

    op.drop_index(op.f('ix_flashcard_reviews_user_id'), table_name='flashcard_reviews')
    op.drop_index(op.f('ix_flashcard_reviews_flashcard_id'), table_name='flashcard_reviews')
    op.drop_table('flashcard_reviews')

    op.drop_index(op.f('ix_quiz_attempts_user_id'), table_name='quiz_attempts')
    op.drop_index(op.f('ix_quiz_attempts_quiz_id'), table_name='quiz_attempts')
    op.drop_table('quiz_attempts')

    op.drop_index(op.f('ix_workspace_sections_document_id'), table_name='workspace_sections')
    op.drop_table('workspace_sections')
