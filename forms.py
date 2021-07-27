from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired

class SignIn(FlaskForm):#this will be more complicated #Derek is gonna do it at some point tho
    username = StringField('Username:',validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm password:', validators=[InputRequired(), EqualTo('password')])
    profile_pic = FileField('Enter a picture you wish to be your profile pic', validators=[FileRequired(),FileAllowed(['jpg','png'],'Images Only!')])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('Look up a book')
    submit = SubmitField('Go!')

class Review(FlaskForm):
    book_name = StringField('Name of Book', validators=[InputRequired()])
    date = DateField('Please enter the date', validators=[InputRequired()])
    rating = IntegerField('Rating out of 10', validators=[InputRequired()])
    review = TextAreaField('Write Your review here:',validators=[InputRequired()])
    submit = SubmitField('Submit')

class EditReview(FlaskForm):
    review = TextAreaField('Description:', validators=[InputRequired()])
    submit = SubmitField('Update!')

class SForm(FlaskForm):
    book_name = StringField('Name of book:')
    author_name = StringField('Author name')
    genre = StringField('Genre')
    submit = SubmitField('Go!')

class ChangeNameForm(FlaskForm):
    old_username = StringField('Tell us your old username', validators=[InputRequired()])
    password = PasswordField('Enter your password', validators=[InputRequired()])
    new_username = StringField('Enter your new username', validators=[InputRequired()])
    submit = SubmitField('Submit')

class BrowseForm(FlaskForm):
    genre = SelectField('Please select a genre', choices=[('classic', 'Classic'),('fiction','Fiction'),('fantasy', 'Fantasy'),('sci-fi', 'Sci-fi'),('childrens','Childrens')])
    submit = SubmitField('Go!')

class ChangePass(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    old_password = PasswordField('Old Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class AddBook(FlaskForm):
    book_name = StringField('Bookname', validators=[InputRequired()])
    genre = SelectField('Please select a genre', choices=[('classic', 'Classic'),('fiction','Fiction'),('fantasy', 'Fantasy'),('sci-fi', 'Sci-fi'),('childrens','Childrens')])
    description = TextAreaField('Description:', validators=[InputRequired()])
    price = DecimalField('Selling price', validators=[InputRequired()])
    author_name = StringField('Author Name:', validators=[InputRequired()])
    cover = FileField('Upload a cover', validators=[FileRequired(),FileAllowed(['jpg','png'],'Images Only!')])
    submit = SubmitField('Enter')

class UpdateInventory(FlaskForm):
    book_name = StringField('Bookname', validators=[InputRequired()])
    author_name = StringField('Author Name', validators=[InputRequired()])
    incInventory = IntegerField('Increase the inventory by:', validators=[InputRequired()])
    submit = SubmitField('Enter')

class UserPic(FlaskForm):
    profile_pic = FileField('Upload a cover', validators=[FileRequired(),FileAllowed(['jpg','png'],'Images Only!')])
    submit = SubmitField('Enter')

class ShippingInfo(FlaskForm):
    first_name = StringField('First Name*', validators=[InputRequired()])
    last_name = StringField('Last Name*', validators=[InputRequired()])
    address1 = StringField('Address line 1 *', validators=[InputRequired()])
    address2 = StringField('Address line 2')
    address3 = StringField('Address line 3*', validators=[InputRequired()])
    country = SelectField('Enter a validate Country*', choices=[('ireland','Ireland'),('britain','Britain'),('france','France')])
    postcode = StringField('Postcode*', validators=[InputRequired()])
    submit = SubmitField('Enter')

class PaymentDetails(FlaskForm):
    cardNum = IntegerField('Enter card number:', validators=[InputRequired()])
    cardHolder = StringField('Enter card holders name:', validators=[InputRequired()])
    cvv = IntegerField('Cvv', validators= [InputRequired()])
    submit = SubmitField('Enter')

class ComplaintForm(FlaskForm):
    typeCom = SelectField('General type of query', choices=[('shipping','Shipping'),('refund','Refund'),('other','Other')])
    date = DateField('Please enter the date', validators=[InputRequired()])
    email = StringField('Enter your email', validators=[InputRequired()])
    complaint = TextAreaField('Write Your issue here:',validators=[InputRequired()])
    submit = SubmitField('Send')

class ResponseForm(FlaskForm):
    response = TextAreaField('Response:',validators=[InputRequired()])
    date = DateField('date', validators=[InputRequired()])
    submit = SubmitField('Send')