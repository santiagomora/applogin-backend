from starlette.requests import\
    Request
from ..exception.auth import\
    AccessForbiddenException
from ..repository.auth import\
    AuthRepository
import jwt
import os


class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)
        auth_header = request.headers.get('Authorization', None)
        if auth_header is None:
            raise AccessForbiddenException('must login to access protected route')
        token = auth_header.split(' ')[1]
        current_user = jwt.decode(token, os.getenv('JWT_SECRET'),
                                  algorithms=["HS256"])
        repo = AuthRepository(request.state.engine)
        user_id = int(current_user['id'])
        if not repo.is_token_valid(user_id, token):
            raise AccessForbiddenException('invalid token')
        request.state.current_user_id = user_id
        await self.app(scope, receive, send)
