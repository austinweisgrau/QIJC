from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField, IntegerField, FieldList, FormField)
from wtforms.validators import (DataRequired, ValidationError, Email,
                                EqualTo, Regexp)
from app.models import User, Paper

class PaperSubmissionForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    volunteering = BooleanField("I'm volunteering to discuss this paper.")
    comments = StringField('Comments (optional)')
    submit = SubmitField('Submit URL')

    def validate_link(self, link):
        if not 'arxiv' in link.data.lower():
            raise ValidationError('Only arxiv.org links are accepted.'
                                  + 'Consider submitting manually.')
        link_str = link.data.split('?')[0]
        paper = Paper.query.filter_by(link=link_str).first()
        if paper is not None:
            print('Validation error raised.')
            raise ValidationError('Link already submitted.')

class ManualSubmissionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    abstract = StringField('Abstract', validators=[DataRequired()])
    volunteering = BooleanField("I'm volunteering to discuss this paper.")
    comments = StringField('Comments (optional)')
    submit = SubmitField('Submit paper.')

    def validate_link(self, link):
        paper = Paper.query.filter_by(link=link.data).first()
        if paper is not None:
            raise ValidationError('Link already submitted.')

    def validate_title(self, title):
        paper = Paper.query.filter_by(title=title.data).first()
        if paper is not None:
            raise ValidationError('Paper with this title already submitted.')
        

class VoteForm(FlaskForm):
    vote_num = IntegerField()
    vote_den = IntegerField()

class FullVoteForm(FlaskForm):
    votes = FieldList(FormField(VoteForm))
    submit = SubmitField('Submit votes.')
