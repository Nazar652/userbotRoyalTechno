from datetime import datetime

from peewee import *
import Levenshtein

db = SqliteDatabase("db.sqlite")

MONTH_SECONDS = 2592000
HOUR_SECONDS = 3600


def calculate_similarity(reference_string, strings):
    total_similarity = 0
    for string in strings:
        distance = Levenshtein.distance(reference_string, string)
        max_length = max(len(reference_string), len(string))
        similarity = (max_length - distance) / max_length
        total_similarity += similarity
    average_similarity = total_similarity / len(strings)
    return average_similarity


class Chat(Model):
    id = IntegerField()
    name = CharField()

    class Meta:
        database = db


class UserMessages:
    users_messages = dict()

    @classmethod
    def new_message(cls, m):
        try:
            cls.users_messages[m.from_user.id].append([m.date, m.text])
        except KeyError:
            cls.users_messages[m.from_user.id] = [[m.date, m.text]]

        if len(cls.users_messages[m.from_user.id]) > 10:
            cls.users_messages[m.from_user.id].pop(0)

    @classmethod
    def check_spam(cls, m):
        single_user_messages = cls.users_messages[m.from_user.id]
        if len(single_user_messages) == 10:
            messages = [i[1] for i in single_user_messages]
            similarity = calculate_similarity(m.text, messages)
            time_differ = single_user_messages[-1][0] - single_user_messages[0][0]
            seconds = time_differ.total_seconds()
            if seconds < HOUR_SECONDS and similarity > 0.5:
                return True
        return False

    @classmethod
    def get_inactive_users(cls):
        user_ids = []
        for u_id, messages in cls.users_messages.items():
            current_time = datetime.now()
            last_message_differ = current_time - messages[-1][0]
            total_seconds = last_message_differ.total_seconds()
            if total_seconds > MONTH_SECONDS:
                user_ids.append(u_id)

        for u_id in user_ids:
            cls.users_messages.pop(u_id)

        return user_ids


Chat.create_table(safe=True)
Chat.insert(id=-1001972778404, name="чееек").on_conflict_ignore().execute()
