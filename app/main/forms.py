from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Regexp
from app.models import User

class PaperSubmissionForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    volunteering = BooleanField("I'm volunteering to discuss this paper.")
    comments = StringField('Comments (optional)')
    submit = SubmitField('Submit URL')

    def validate_link(self, link):
        if not 'arxiv' in link.data.lower():
            raise ValidationError('Only arxiv.org links are accepted.'
                                  + 'Consider submitting manually.')

class ManualSubmissionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    abstract = StringField('Abstract', validators=[DataRequired()])
    volunteering = BooleanField("I'm volunteering to discuss this paper.")
    comments = StringField('Comments (optional)')
    submit = SubmitField('Submit paper.')
