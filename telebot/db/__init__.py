from traceback import print_exc
from typing import List

from mongoengine import DynamicDocument, IntField, ListField, StringField


# db classes


class User(DynamicDocument):
    user_id = IntField(required=True, primary_key=True)
    words = ListField(StringField())


# helper methods


def add_word_for_user(user: int, word: str) -> bool:
    """
    Add a word into the list of words a user has studied
    :param user: ID of the user
    :param word: the word to be added
    :return: True if successfully added, else False
    """
    try:
        user_obj = User.objects(user_id=user).first()

        if user_obj:
            # The user object already exists
            user_obj.words = user_obj.words + [word]
            user_obj.save()
        else:
            # make new object
            User(user_id=user, words=[word]).save()

        return True

    except:
        print_exc()
        return False


def get_words_for_user(user: int) -> List[str]:
    """
    get list of words that user has already studied
    :param user: ID of the user
    :return: List of all the words
    """
    try:
        return User.objects(user_id=user).first().words
    except:
        print_exc()
        return []


def clear_words_for_user(user: int) -> bool:
    """
    Clear list of all words for a user
    :param user: ID of the user
    :return: True if all words cleared, else False
    """
    try:
        user_list = User.objects(user_id=user).first()
        if user_list:
            user_list.words = []
            user_list.save()

        return True

    except:
        print_exc()
        return False
