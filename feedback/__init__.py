from flask import Flask

from config import Config
from feedback.repositories import RelationSearchRepo, FeedbackRepo
from feedback.storage import RedmineStorage, InMemoryStorage


def _create_storage(config):
    redmine_storage = RedmineStorage(config['REDMINE_URL'], config['REDMINE_KEY'])
    assignments = redmine_storage.all_assignments(from_date=config['LOAD_ASSIGNMENT_FROM']).assignments()

    print('Storage is load')

    return InMemoryStorage(assignments)


app = Flask(__name__)
app.config.from_object(Config)

storage = _create_storage(app.config)
rel_search_repo = RelationSearchRepo()
feedback_repo = FeedbackRepo()

from feedback import routes
