from ..controller.auth import \
    login,\
    logout,\
    register
from ..middleware.auth import\
    AuthMiddleware
from ..middleware.validate_payload import\
    ValidatePayloadMiddleware
from starlette.routing import\
    Mount,\
    Route
from starlette.middleware import\
    Middleware
from ..utils.validator import\
    required,\
    valid_regex


routes = [Route("/login", login,
                name='login', methods=['POST'],
                middleware=[Middleware(ValidatePayloadMiddleware,
                                       validation={"email": (required(),
                                                             valid_regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                                                         "must be a valid email address"), ),
                                                   "password": (required(), )})]),
          Route("/register", register,
                name='register', methods=['POST'],
                middleware=[Middleware(ValidatePayloadMiddleware,
                                       validation={"name": (required(), ),
                                                   "lastname": (required(), ),
                                                   "email": (required(),
                                                             valid_regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                                                         "must be a valid email address"), ),
                                                   "password": (required(),
                                                                valid_regex(r'[a-z]',
                                                                            "must have at least one lowercase letter"),
                                                                valid_regex(r'[A-Z]',
                                                                            "must have at least one uppercase letter"),
                                                                valid_regex(r'(\-|\_|\!|\?|\.|\*|\@)',
                                                                            "must have at least a special character: -, _, !, ?, ., *, @]"),
                                                                valid_regex(r'.{10,}',
                                                                            "must have at least 10 characters long"), )})]),
          Mount("/logout", routes=[Route("/", logout, name='logout')],
                middleware=[Middleware(AuthMiddleware)])]
