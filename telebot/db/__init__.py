from typing import List

from mongoengine import DynamicDocument, IntField, ListField, StringField


# db classes


class User(DynamicDocument):
    id = IntField(required=True)
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
        user_list = User.objects(id=user)

        if user_list:
            # The user object already exists
            user_list[0].words = user_list[0].words + [word]
            user_list[0].save()
        else:
            # make new object
            User(id=user, words=[word]).save()

        return True

    except:
        return False


def get_words_for_user(user: int) -> List[str]:
    """
    get list of words that user has already studied
    :param user: ID of the user
    :return: List of all the words
    """
    try:
        return User.objects(id=user)[0].words
    except:
        return []
