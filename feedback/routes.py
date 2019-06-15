from flask import render_template

from feedback import app
from feedback.forms import EmployeeRelationForm, CreateFeedbackForm
from feedback.mediator import get_all_employees, get_all_relations, save_relation_search, \
    get_all_rel_search, get_employee, get_rel_search, save_feedback


@app.route('/relation/search', methods=['GET', 'POST'])
def relation_search():
    relations = None
    employees = get_all_employees()

    form = EmployeeRelationForm()
    form.employee_id.choices = [(em.id, em.name) for em in employees]

    if form.validate_on_submit():
        employee = get_employee(form.employee_id.data)
        relations = get_all_relations(
            employee=get_employee(form.employee_id.data),
            exclude_project_ids=app.config['DEFAULT_EXCLUDED_PROJECT_IDS'],
            from_date=form.from_date.data,
            to_date=form.to_date.data,
            min_count_days=form.min_count_workdays.data
        )

        if form.submit_save_result.data:
            save_relation_search(
                employee=employee,
                exclude_project_ids=app.config['DEFAULT_EXCLUDED_PROJECT_IDS'],
                from_date=form.from_date.data,
                to_date=form.to_date.data,
                min_count_days=form.min_count_workdays.data
            )

    return render_template('relation_search.html', title='Relation Search', form=form, relations=relations)


@app.route('/', methods=['GET'])
@app.route('/relation/list', methods=['GET'])
def relation_search_list():
    rel_search_dict = get_all_rel_search()
    return render_template('rel_search_list.html', title='Relation Search List', rel_search_dict=rel_search_dict)


@app.route('/relation/<int:id>', methods=['GET'])
def get_relation_search(id):
    rel_search = get_rel_search(id)
    relations = get_all_relations(
        employee=rel_search.employee,
        exclude_project_ids=rel_search.exclude_project_ids,
        from_date=rel_search.from_date,
        to_date=rel_search.to_date,
        min_count_days=rel_search.min_count_days
    )

    return render_template('get_rel_search.html', titile='Relation History',
                           rel_search=rel_search, rel_search_id=id, relations=relations)


@app.route('/relation/<int:id>/mail', methods=['GET', 'POST'])
def create_mail(id):
    form = CreateFeedbackForm()
    if form.validate_on_submit():
        save_feedback(id, form.content.data)
        # install flask-mail & setting & send mail
        # contact search into yabt with employee_id = user.id in redmine
        return render_template('successful_send_mail.html', title='Successful Sen Mail')

    return render_template('create_mail.html', title='Create Mail', form=form)
