from ..utils.error_bag import\
    ErrorBag
from starlette.requests import\
    Request
from ..exception.validation import\
    CollectableException,\
    InvalidRequestBodyException
from ..exception.validation import\
    RequestValidationException
import json


class ValidatePayloadMiddleware:
    def __init__(self, app, *, validation, apply_on):
        self._validation = validation
        self._apply_on = apply_on
        self.app = app
        errbag = ErrorBag()
        for field_name, rules in self._validation.items():
            try:
                if len(rules) == 0:
                    raise CollectableException(field_name, "validation rules cant be empty")
            except CollectableException as e:
                errbag.add(e)
        if errbag.has_errors():
            raise Exception(f'malformed validation rules\n{str(errbag)}')

    def validate_payload(self, payload):
        errbag = ErrorBag()
        for field_name, value in self._validation.items():
            for rule in self._validation.get(field_name, []):
                try:
                    rule(field_name, payload)
                except CollectableException as e:
                    errbag.add(e)
        if errbag.has_errors():
            raise RequestValidationException(errbag)

    async def validate_request_body(self, scope, receive, send):
        body = b""

        async def receive_request_body():
            nonlocal body, self
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body", False):
                try:
                    self.validate_payload(json.loads(body.decode().replace("'", '"')))
                except json.JSONDecodeError as e:
                    raise InvalidRequestBodyException(str(e))
            return message
        await self.app(scope, receive_request_body, send)

    async def validate_request_query_params(self, scope, receive, send):
        request = Request(scope, receive)
        self.validate_payload(request.query_params)
        await self.app(scope, receive, send)

    async def __call__(self, scope, receive, send):
        if self._apply_on == 'body':
            await self.validate_request_body(scope, receive, send)
        elif self._apply_on == 'query_params':
            await self.validate_request_query_params(scope, receive, send)

