

class CollectableException(Exception):
    def __init__(self, name, e):
        self.name = name
        super().__init__(e)


class RequestValidationException(Exception):
    def __init__(self, error_bag):
        self.error_bag = error_bag


class InvalidRequestBodyException(Exception):
    pass
