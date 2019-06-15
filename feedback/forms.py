from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class EmployeeRelationForm(FlaskForm):
    from_date = DateField('From Date', validators=[DataRequired()])
    to_date = DateField('To Date')
    employee_id = SelectField('Employee', validators=[DataRequired()], coerce=int)
    min_count_workdays = IntegerField('Minimal count workdays', validators=[NumberRange(min=1)])
    submit_search = SubmitField('Search')
    submit_save_result = SubmitField('Save Result')


class CreateFeedbackForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')
