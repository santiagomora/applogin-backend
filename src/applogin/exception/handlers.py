from .validation import\
    RequestValidationException,\
    InvalidRequestBodyException
from .auth import\
    AccessForbiddenException
from .model import\
    ModelNotFoundException
from starlette.responses import\
    JSONResponse
from starlette.status import\
    HTTP_500_INTERNAL_SERVER_ERROR,\
    HTTP_400_BAD_REQUEST,\
    HTTP_404_NOT_FOUND,\
    HTTP_403_FORBIDDEN
from jwt.exceptions import\
    InvalidTokenError
from sqlalchemy.orm.exc import\
    NoResultFound
from sqlalchemy.exc import\
    IntegrityError


def request_validation_exception_handler(request, exc):
    return JSONResponse({'message': 'invalid_request_body',
                         'type': 'validation_error',
                         'detail': exc.error_bag.errors},
                        status_code=HTTP_400_BAD_REQUEST)


def any_exception_handler(request, exc):
    # la idea es loggear
    print(str(exc))
    return JSONResponse({'detail': 'internal_error',
                         'type': 'server_error',
                         'message': str(exc)},
                        status_code=HTTP_500_INTERNAL_SERVER_ERROR)


def invalid_body_exception_handler(request, exc):
    print(str(exc))
    return JSONResponse({'message': 'cannot_parse_request_body',
                         'type': 'request_error',
                         'detail': None},
                        status_code=HTTP_400_BAD_REQUEST)


def model_not_found_exception_handler(request, exc):
    return JSONResponse({'message': 'model_not_found',
                         'type': 'sql_error',
                         'detail': str(exc)},
                        status_code=HTTP_404_NOT_FOUND)


def access_forbidden_exception_handler(request, exc):
    return JSONResponse({'message': 'access_forbidden',
                         'type': 'access_error',
                         'detail': str(exc)},
                        status_code=HTTP_403_FORBIDDEN)


def integrity_error_handler(request, exc):
    return JSONResponse({'message': 'integrity_error',
                         'type': 'sql_error',
                         'detail': str(exc)},
                        status_code=HTTP_400_BAD_REQUEST)


exception_handlers = {Exception: any_exception_handler,
                      IntegrityError: integrity_error_handler,
                      RequestValidationException: request_validation_exception_handler,
                      InvalidRequestBodyException: invalid_body_exception_handler,
                      NoResultFound: model_not_found_exception_handler,
                      InvalidTokenError: access_forbidden_exception_handler,
                      AccessForbiddenException: access_forbidden_exception_handler}
