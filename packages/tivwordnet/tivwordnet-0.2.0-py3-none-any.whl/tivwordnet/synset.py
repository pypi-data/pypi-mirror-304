class Synset:
    """Synset we kwaseer mga a yon a kwagh i or u fan evese.

    Methods:
        get_words(): mterem ka mga Word objects
        ga a kwagh i u fan evese.
    """

    def __init__(self, sid, words):
        self._words = words
        self._id = sid

    def get_words(self):
        return self._words

    def __eq__(self, other):
        return self._id == other._id and self._words == other._words

    def __hash__(self):
        return self._id
