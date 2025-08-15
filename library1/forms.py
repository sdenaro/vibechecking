from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Optional

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publish_date = DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CheckoutForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    book_id = IntegerField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Checkout')

class ReturnForm(FlaskForm):
    checkout_id = IntegerField('Checkout ID', validators=[DataRequired()])
    submit = SubmitField('Return')
