from feedback.models import Project, Employee, Assignment, Feedback
from datetime import date


class TestProject(object):

    def test_creation(self):
        project = Project(100, 'Feedback Project')
        assert project.id == 100
        assert project.name == 'Feedback Project'


class TestEmployee(object):

    def test_creation(self):
        employee = Employee(10, 'Alice')
        assert employee.id == 10
        assert employee.name == 'Alice'


class TestAssignment(object):

    def test_creation(self):
        project = Project(100, 'Project')
        employee = Employee(10, 'John')
        assignment = Assignment(date.today(), project, employee)
        assert assignment.workday == date.today()
        assert assignment.project.id == 100
        assert assignment.project.name == 'Project'
        assert assignment.employee.id == 10
        assert assignment.employee.name == 'John'


class TestFeedback(object):

    def test_creation(self):
        employee = Employee(11, 'James')
        colleague1 = Employee(14, 'Alice')
        feedback = Feedback(15, employee, [colleague1], 'Send content')
        assert feedback.id == 15
        assert feedback.employee.id == 11
        assert feedback.employee.name == 'James'
        assert feedback.colleagues[0].id == 14
        assert feedback.colleagues[0].name == 'Alice'
        assert feedback.content == 'Send content'
