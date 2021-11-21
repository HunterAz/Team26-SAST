from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField

class AnnouncementForm(FlaskForm):
    body = TextAreaField("Description", [validators.Length(
        max=1000), validators.DataRequired()], render_kw={"placeholder": "Type your announcement here"})