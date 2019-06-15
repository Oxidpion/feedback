"""Module content entity."""
from collections import namedtuple


class Employee(object):

    def __init__(self, id, name):
        """Information about employee.

        Args:
            id: `int`
            name: `str`
        """
        self.id = id
        self.name = name


class Project(object):

    def __init__(self, id, name):
        """Information about project which work at employee.

        Args:
            id: `int`
            name: `str`
        """
        self.id = id
        self.name = name


class Assignment(object):

    def __init__(self, workday, project, employee):
        """Information about assignment employee to project.

        Args:
            workday: `datetime.date`
            project: `Project`
            employee: `Employee`
        """
        self.workday = workday
        self.project = project
        self.employee = employee


class Feedback(object):

    def __init__(self, employee, colleagues, content):
        """Employee's feedback send to colleagues.

        Args:
            employee: `Employee`
            colleagues: `list` of `Employee`
            content: `str`
        """
        self.employee = employee
        self.colleagues = colleagues
        self.content = content


class AssignmentList(object):

    def __init__(self, assignments):
        self._assignments = assignments

    def employees(self):
        return set([assign.employee for assign in self._assignments])

    def projects(self):
        return set([assign.project for assign in self._assignments])

    def workdays(self):
        return set([assign.workday for assign in self._assignments])

    def assignments(self):
        return self._assignments


"""Relation bitwise employee and colleagues. 

Args:
    employee: `Employee`
    colleagues: `list` of `Employee`
    project: `Project`
    count_days: `int`
"""
RelationColleague = namedtuple('RelationColleague', ['employee', 'colleague', 'project', 'count_days'])
