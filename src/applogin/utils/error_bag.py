import pprint


class ErrorBag:
    def __init__(self):
        self.errors = {}

    def add(self, exc):
        if exc.name in self.errors:
            self.errors[exc.name].append(str(exc))
        else:
            self.errors[exc.name] = [str(exc)]

    def has_errors(self):
        return len(self.errors.keys()) > 0

    def __str__(self):
        return pprint.pformat(self.errors)
