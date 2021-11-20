from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField

class ThreadForm(FlaskForm):
    subject = StringField(
        "Thread title", [validators.Length(max=100), validators.DataRequired()], render_kw={"placeholder": "Name of thread"})
    body = TextAreaField("Description", [validators.Length(
        max=1000), validators.DataRequired()], render_kw={"placeholder": "Type your description here"})
