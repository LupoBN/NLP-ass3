class ContextStrategy(object):

    def __init__(self):
        pass

    def get_context(self, sentence):
        """

        :param sentence: a list, containing strings of a single word in the Depparse format.
        :return: context: a list, containing strings that represent the context (according to the strategy).
        """
        raise NotImplementedError