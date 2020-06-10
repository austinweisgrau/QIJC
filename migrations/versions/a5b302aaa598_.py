"""empty message

Revision ID: a5b302aaa598
Revises: 731d962d005f
Create Date: 2020-06-09 18:54:28.454228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5b302aaa598'
down_revision = '731d962d005f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('paper',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('link', sa.String(length=140), nullable=True),
    sa.Column('abstract', sa.String(length=512), nullable=True),
    sa.Column('authors', sa.String(length=256), nullable=True),
    sa.Column('voted', sa.DateTime(), nullable=True),
    sa.Column('score_n', sa.Integer(), nullable=True),
    sa.Column('score_d', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=256), nullable=True),
    sa.Column('subber_id', sa.Integer(), nullable=True),
    sa.Column('volunteer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subber_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('link')
    )
    with op.batch_alter_table('paper', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_paper_timestamp'), ['timestamp'], unique=False)

    op.drop_table('sqlite_sequence')
    op.drop_table('User')
    op.drop_table('announcement')
    op.drop_table('comments')
    op.drop_table('cat_comments')
    op.drop_table('requests')
    op.drop_table('Paper')
    op.drop_table('actions')
    op.drop_table('weeks')
    op.drop_table('abstracts')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.NullType(), nullable=True),
    sa.Column('salt', sa.NullType(), nullable=True),
    sa.Column('passhash', sa.NullType(), nullable=True),
    sa.Column('firstname', sa.NullType(), nullable=True),
    sa.Column('lastname', sa.NullType(), nullable=True),
    sa.Column('email', sa.NullType(), nullable=True),
    sa.Column('points', sa.NullType(), nullable=True),
    sa.Column('diligence', sa.NullType(), nullable=True),
    sa.Column('nickname', sa.NullType(), nullable=True),
    sa.Column('retired', sa.NullType(), nullable=True)
    )
    op.create_table('abstracts',
    sa.Column('submitter', sa.NullType(), nullable=True),
    sa.Column('title', sa.NullType(), nullable=True),
    sa.Column('abstract', sa.NullType(), nullable=True),
    sa.Column('authors', sa.NullType(), nullable=True),
    sa.Column('journalref', sa.NullType(), nullable=True),
    sa.Column('subtime', sa.NullType(), nullable=True),
    sa.Column('votenumerator', sa.NullType(), nullable=True),
    sa.Column('votedenominator', sa.NullType(), nullable=True),
    sa.Column('votefraction', sa.NullType(), nullable=True),
    sa.Column('url', sa.NullType(), nullable=True),
    sa.Column('id', sa.NullType(), nullable=True),
    sa.Column('week', sa.NullType(), nullable=True),
    sa.Column('volunteer', sa.NullType(), nullable=True)
    )
    op.create_table('weeks',
    sa.Column('number', sa.NullType(), nullable=True),
    sa.Column('date', sa.NullType(), nullable=True),
    sa.Column('presenter', sa.NullType(), nullable=True),
    sa.Column('topic', sa.NullType(), nullable=True),
    sa.Column('filename', sa.NullType(), nullable=True)
    )
    op.create_table('actions',
    sa.Column('type', sa.NullType(), nullable=True),
    sa.Column('week', sa.NullType(), nullable=True),
    sa.Column('user', sa.NullType(), nullable=True),
    sa.Column('topic', sa.NullType(), nullable=True)
    )
    op.create_table('Paper',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.TEXT(), nullable=True),
    sa.Column('timestamp', sa.TEXT(), nullable=True),
    sa.Column('link', sa.TEXT(), nullable=True),
    sa.Column('abstract', sa.TEXT(), nullable=True),
    sa.Column('authors', sa.TEXT(), nullable=True),
    sa.Column('voted', sa.INTEGER(), nullable=True),
    sa.Column('score_n', sa.INTEGER(), nullable=True),
    sa.Column('score_d', sa.INTEGER(), nullable=True),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('subber_id', sa.INTEGER(), nullable=True),
    sa.Column('volunteer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['subber_id'], ['User.id'], ),
    sa.ForeignKeyConstraint(['volunteer_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requests',
    sa.Column('username', sa.NullType(), nullable=True),
    sa.Column('salt', sa.NullType(), nullable=True),
    sa.Column('passhash', sa.NullType(), nullable=True),
    sa.Column('firstname', sa.NullType(), nullable=True),
    sa.Column('lastname', sa.NullType(), nullable=True),
    sa.Column('email', sa.NullType(), nullable=True)
    )
    op.create_table('cat_comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.NullType(), nullable=True),
    sa.Column('comment', sa.NullType(), nullable=True),
    sa.Column('commenter', sa.NullType(), nullable=True)
    )
    op.create_table('announcement',
    sa.Column('presenter', sa.NullType(), nullable=True),
    sa.Column('text', sa.NullType(), nullable=True)
    )
    op.create_table('User',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.TEXT(), nullable=True),
    sa.Column('firstname', sa.TEXT(), nullable=True),
    sa.Column('lastname', sa.TEXT(), nullable=True),
    sa.Column('email', sa.TEXT(), nullable=True),
    sa.Column('password_hash', sa.TEXT(), nullable=True),
    sa.Column('admin', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    with op.batch_alter_table('paper', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_paper_timestamp'))

    op.drop_table('paper')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
