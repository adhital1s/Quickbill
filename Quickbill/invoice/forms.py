from  flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField,BooleanField,PasswordField,DateField,SelectField,ValidationError,FieldList, FormField,widgets
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Sign In')

class ReportForm(FlaskForm):
    this_week=SubmitField('This Week')
    last_week=SubmitField('Last Week')
    january=SubmitField('January')
    february=SubmitField('February')
    march=SubmitField('March')
    april=SubmitField('April')
    may=SubmitField('May')
    june=SubmitField('June')
    july=SubmitField('July')
    august=SubmitField('August')
    september=SubmitField('September')
    october=SubmitField('October')
    november=SubmitField('November')
    december=SubmitField('December')
    today=SubmitField('Today')
    this_month=SubmitField('This month')
    yesterday=SubmitField('Yesterday')

class SignupForm(FlaskForm):
    firstname=StringField('First Name: ',validators=[DataRequired()])
    lastname=StringField('Last Name: ',validators=[DataRequired()])
    username=StringField('Username: ',validators=[DataRequired()])
    password=PasswordField('Password: ',validators=[Length(min=5,max=20)])
    confirm_password=PasswordField('Confirm Password: ',validators=[Length(min=5,max=20),EqualTo('password',message='Password Must Match')])
    signup=SubmitField('Sign Up')


class MainForm(FlaskForm):
    name=StringField('Costumer Name: ',validators=[DataRequired()])
    item = StringField('Item',validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    alternate_quantity = StringField('Alt. Quantity')
    quantity=StringField('Quantity',validators=[DataRequired()])
    rate = StringField('Rate',validators=[DataRequired()])
    per = StringField('Per',validators=[DataRequired()])
    amount=StringField('Amount',validators=[DataRequired()])
    total_amount=StringField('Total Amount',validators=[DataRequired()])
    paid_amount=IntegerField('Paid Amount',validators=[DataRequired()])
    discount=IntegerField('Discount')
    remaning_amount = IntegerField('Remaning Amount',validators=[DataRequired()])
    submit=SubmitField('Submit')
    
class RecieveForm(FlaskForm):
    paid_amount = IntegerField('Paid Amount')
    submit = SubmitField('Submit')
    
class AddItemForm (FlaskForm):
    item_name=StringField('Item Name')
    item_brand=StringField('Brand')
    item_category=StringField('Category')
    item_price=IntegerField('Cost Price')
    item_quantity=IntegerField('Quantity')
    submit=SubmitField('Submit')


class AddClientForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    companyname = StringField('Company Name')
    email = StringField('Email')
    primary_phone = StringField('Primary Phone No')
    secondary_phone = StringField('Secondary Phone No.')
    address = StringField('Address')
    pan_no = StringField('Pan No')
    submit=SubmitField('Submit')