from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class PaperSubmissionForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    volunteering = BooleanField("I'm volunteering to discuss this paper.")
    comments = StringField('Comments (optional)')
    submit = SubmitField('Submit URL')
