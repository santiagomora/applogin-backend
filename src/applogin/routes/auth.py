from ..controller.auth import \
    login,\
    logout,\
    register,\
    test
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
                                       apply_on='body',
                                       validation={"email": (required(),
                                                             valid_regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                                                                         "must be a valid email address"), ),
                                                   "password": (required(), )})]),
          Route("/register", register,
                name='register', methods=['POST'],
                middleware=[Middleware(ValidatePayloadMiddleware,
                                       apply_on='body',
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
          Mount("/",
                routes=[Route("/logout", logout, name='logout'),
                        Route("/test", test, name='test',
                              middleware=[Middleware(ValidatePayloadMiddleware,
                                                     apply_on='query_params',
                                                     validation={"route": (required(), )})])],
                middleware=[Middleware(AuthMiddleware)])]
