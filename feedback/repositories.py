from collections import namedtuple

RelationSearch = namedtuple(
    'RelationSearch', ['employee', 'exclude_project_ids', 'from_date', 'to_date', 'min_count_days', 'created_at'])


class RelationSearchRepo(object):

    def __init__(self):
        self.__relation_searches = {}

    def save(self, relation_search):
        last_id = len(self.__relation_searches) + 1
        self.__relation_searches[last_id] = relation_search
        return last_id

    def get(self, id):
        return self.__relation_searches.get(id, None)

    def all(self):
        return self.__relation_searches


class FeedbackRepo(object):

    def __init__(self):
        self.__feedback = {}

    def save(self, feedback):
        last_id = len(self.__feedback) + 1
        self.__feedback[last_id] = feedback
        return last_id

    def get(self, id):
        return self.__feedback.get(id, None)
