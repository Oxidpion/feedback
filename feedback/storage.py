from redminelib import Redmine

from .models import AssignmentList, Project, Employee, Assignment


class InMemoryStorage(object):

    def __init__(self, assignments):
        self.__assignments = assignments

    def all_employee(self):
        """

        Returns:
            set of `feedback.models.Employee`
        """
        return set([assignment.employee for assignment in self.__assignments])

    def get_employee(self, employee_id):
        """

        Args:
            employee_id: `int`

        Returns:
            None or `feedback.models.Employee`
        """
        it = (ass.employee for ass in self.__assignments if ass.employee.id == employee_id)
        return next(it, None)

    def all_assignments(self, employee=None, project=None, workdays=None, from_date=None, to_date=None):
        """

        Args:
            employee:  `feedback.models.Employee`
            project:   `feedback.models.Project`
            workdays:  `datetime.date`
            from_date: `datetime.date`
            to_date:   `datetime.date`

        Returns:
            `feedback.models.AssignmentList`
        """
        assignments = self.__assignments

        if employee is not None:
            assignments = [ass for ass in assignments if ass.employee.id == employee.id]

        if project is not None:
            assignments = [ass for ass in assignments if ass.project.id == project.id]

        if from_date is not None:
            assignments = [ass for ass in assignments if ass.workday >= from_date]

        if to_date is not None:
            assignments = [ass for ass in assignments if ass.workday <= to_date]

        if workdays is not None and len(workdays) > 0:
            assignments = [ass for ass in assignments if ass.workday in workdays]

        return AssignmentList(assignments)


class RedmineStorage(object):

    def __init__(self, redmine_url, redmine_key):
        self.__redmine = Redmine(redmine_url, key=redmine_key)
        self.__projects = dict()
        self.__employees = dict()

    def all_employee(self):
        """

        Returns:
            set of `feedback.models.Employee`
        """
        employees = list()
        for user in self.__redmine.user.filter(status=1):
            employee_id = getattr(user, 'id', None)
            employee_name = getattr(user, 'name', None)
            if employee_id is not None and employee_name is not None:
                employee = Employee(employee_id, employee_name)
                employees.append(employee)

        return employees

    def get_employee(self, employee_id):
        """

        Args:
            employee_id: `int`

        Returns:
            None or `feedback.models.Employee`
        """
        user = self.__redmine.get(employee_id)
        if hasattr(user, 'id') and hasattr(user, 'name'):
            return Employee(user.id, user.name)

        return None

    def all_assignments(self, employee=None, project=None, workdays=None, from_date=None, to_date=None):
        """

        Args:
            employee:  `feedback.models.Employee`
            project:   `feedback.models.Project`
            workdays:  `datetime.date`
            from_date: `datetime.date`
            to_date:   `datetime.date`

        Returns:
            `feedback.models.AssignmentList`
        """
        time_entries = self.__redmine.time_entry.filter(
            user_id=getattr(employee, 'id', None),
            project_id=getattr(project, 'id', None),
            from_date=from_date,
            to_date=to_date,
        )

        assignments = list()
        for time_entry in time_entries:
            assignment = self.__to_assignment(time_entry, employee=employee, project=project)
            if assignment is not None:
                assignments.append(assignment)

        if workdays is not None and len(workdays) > 0:
            assignments = [ass for ass in assignments if ass.workday in workdays]

        return AssignmentList(assignments)

    def __to_assignment(self, time_entry, employee=None, project=None):

        if project is None:
            project = self.__to_project(time_entry)

        if employee is None:
            employee = self.__to_employee(time_entry)

        workday = getattr(time_entry, 'spent_on', None)

        if project is not None and workday is not None and employee is not None:
            return Assignment(workday=workday, project=project, employee=employee)

        return None

    def __to_project(self, time_entry):

        if not hasattr(time_entry, 'project'):
            return None

        project_id = time_entry.project.id
        project_name = time_entry.project.name

        project = self.__projects.get(project_id)
        if project is None:
            project = Project(project_id, project_name)
            self.__projects[project_id] = project

        return project

    def __to_employee(self, time_entry):

        if not hasattr(time_entry, 'user'):
            return None

        employee_id = time_entry.user.id
        employee_name = time_entry.user.name

        employee = self.__employees.get(employee_id)
        if employee is None:
            employee = Employee(employee_id, employee_name)
            self.__employees[employee_id] = employee

        return employee
