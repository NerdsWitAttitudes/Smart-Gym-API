class RootFactory(dict):
    def __init__(self, request):
        self.requires_oauth = False
        self.request = request
        self.__name__ = None
        self.__parent__ = None
