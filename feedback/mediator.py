from datetime import datetime
from operator import attrgetter

from feedback import storage, rel_search_repo, feedback_repo
from feedback.models import RelationColleague, Feedback
from feedback.repositories import RelationSearch


def get_employee(id):
    return storage.get_employee(id)


def get_all_employees():
    employees = storage.all_employee()
    return sorted(employees, key=attrgetter('name'))


def get_all_relations(employee=None, exclude_project_ids=None, from_date=None, to_date=None, min_count_days=None):
    if employee is None:
        return list()

    projects = get_projects(employee, exclude_project_ids, from_date, to_date)
    relations = list()
    for project in projects:
        workdays = get_workdays(employee, project, from_date=from_date, to_date=to_date)
        colleagues = get_colleagues(employee, project, workdays)

        for colleague in colleagues:
            together_workdays = get_workdays(colleague, project, workdays=workdays)

            relation = RelationColleague(employee, colleague, project, len(together_workdays))
            relations.append(relation)

    if min_count_days is not None:
        relations = [r for r in relations if r.count_days >= min_count_days]

    return relations


def get_projects(employee, exclude_project_ids=None, from_date=None, to_date=None):
    projects = storage.all_assignments(
        employee=employee,
        from_date=from_date,
        to_date=to_date,
    ).projects()

    if exclude_project_ids is not None:
        projects = [p for p in projects if p.id not in exclude_project_ids]

    return projects


def get_workdays(employee, project, workdays=None, from_date=None, to_date=None):
    return storage.all_assignments(
        employee=employee,
        project=project,
        workdays=workdays,
        from_date=from_date,
        to_date=to_date
    ).workdays()


def get_colleagues(employee, project, workdays):
    colleagues = storage.all_assignments(project=project, workdays=workdays).employees()
    return [c for c in colleagues if c.id != employee.id]


def save_relation_search(employee=None, exclude_project_ids=None, from_date=None, to_date=None, min_count_days=None):
    rel_search = RelationSearch(
        employee=employee,
        exclude_project_ids=exclude_project_ids,
        from_date=from_date,
        to_date=to_date,
        min_count_days=min_count_days,
        created_at=datetime.now()
    )
    rel_search_repo.save(rel_search)


def get_all_rel_search():
    return rel_search_repo.all()


def get_rel_search(id):
    return rel_search_repo.get(id)


def save_feedback(relation_id, content_feedback):
    rel_search = rel_search_repo.get(relation_id)
    relations = get_all_relations(
        employee=rel_search.employee,
        exclude_project_ids=rel_search.exclude_project_ids,
        from_date=rel_search.from_date,
        to_date=rel_search.to_date,
        min_count_days=rel_search.min_count_days
    )
    colleagues = map(attrgetter('colleague'), relations)

    feedback = Feedback(employee=rel_search.employee, colleagues=colleagues, content=content_feedback)
    feedback_repo.save(feedback)
