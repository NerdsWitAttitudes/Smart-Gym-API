class BaseFactory(dict):

    def __init__(self, parent, name):
        self.requires_oauth = False
        self.__parent__ = parent
        self.__name__ = name
        self.request = None
        if parent is not None:
            self.request = parent.request
