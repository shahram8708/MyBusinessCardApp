from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FieldList, FileField, FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class VCardForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    phone = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    website = StringField('Website (Optional)', validators=[Optional()])
    address = TextAreaField('Business Address', validators=[DataRequired()])

    
    linkedin = StringField('LinkedIn Profile (Optional)', validators=[Optional()])
    twitter = StringField('Twitter Profile (Optional)', validators=[Optional()])
    instagram = StringField('Instagram Profile (Optional)', validators=[Optional()])
    facebook = StringField('Facebook Profile (Optional)', validators=[Optional()])

    
    about = TextAreaField('About Your Business', validators=[Optional(), Length(max=500)])

    
    monday = StringField('Monday Hours', validators=[Optional()])
    tuesday = StringField('Tuesday Hours', validators=[Optional()])
    wednesday = StringField('Wednesday Hours', validators=[Optional()])
    thursday = StringField('Thursday Hours', validators=[Optional()])
    friday = StringField('Friday Hours', validators=[Optional()])
    saturday = StringField('Saturday Hours', validators=[Optional()])
    sunday = StringField('Sunday Hours', validators=[Optional()])

    
    banner_image = FileField('Banner Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    gallery_images = FieldList(FileField('Gallery Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]), min_entries=1)
    description = TextAreaField('User Description (Optional)', validators=[Optional(), Length(max=500)])
    profile_photo = FileField('Profile Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])

    service_titles = FieldList(StringField('Service Title', validators=[DataRequired()]), min_entries=1)
    service_descriptions = FieldList(TextAreaField('Service Description', validators=[DataRequired()]), min_entries=1)
    service_images = FieldList(FileField('Service Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]), min_entries=1)

    submit = SubmitField('Create V Card')
