
class ModelNotFoundException(Exception):
    def __init__(self, model_name, e):
        self.model_name = model_name
        super().__init__(e)
