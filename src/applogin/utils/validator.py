import re
from ..exception.validation import\
    CollectableException


class BaseValidator:
    def __call__(self, field_name, payload):
        pass


class required(BaseValidator):
    def __call__(self, field_name, payload):
        if field_name not in payload:
            raise CollectableException(field_name, "is required")


class valid_regex(BaseValidator):
    def __init__(self, regex, validation_msg):
        self._regex = regex
        self._validation_msg = validation_msg

    def __call__(self, field_name, payload):
        if field_name not in payload:
            return
        if not isinstance(payload[field_name], str):
            raise CollectableException(field_name, "must be a string")
        if not re.search(self._regex, payload[field_name]):
            raise CollectableException(field_name, self._validation_msg)
