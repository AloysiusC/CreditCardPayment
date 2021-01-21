 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional
from wtforms.fields.html5 import DateField
from datetime import date
from wtforms_components import DateTimeField, DateRange

class DateValid(object):
    def __call__(self, form, field):
        if(field.data < date.today()):
            raise ValidationError('Enter a correct date!')
        else:
            return True



class RegistrationForm(FlaskForm):

    card_no = StringField('Credit Card No.', validators=[DataRequired(), Length(min=11, max=11)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    exp_date = DateField('Expiration Date', validators=[DataRequired()])
    password = PasswordField('Password (Optional 3-digit)', validators=[Optional(), Length(min=3, max=3)])
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Pay')