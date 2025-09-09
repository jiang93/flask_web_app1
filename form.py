#/blog_post/form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import data_required

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()])
    text = TextAreaField('Text', validators=[data_required()])
    submit = SubmitField('Post')