from starlette.responses import\
    JSONResponse
from ..repository.auth import\
    AuthRepository
from datetime import\
    datetime,\
    timedelta
from zoneinfo import\
    ZoneInfo
from ..exception.validation import\
    InvalidRequestBodyException,\
    RequestValidationException
from ..utils.error_bag import\
    ErrorBag
from ..exception.auth import\
    AccessForbiddenException
import json
import jwt
import os


async def login(request):
    try:
        payload = await request.json()
    except json.JSONDecodeError as e:
        raise InvalidRequestBodyException(str(e))
    repo = AuthRepository(request.state.engine)
    if not repo.is_password_valid(payload['email'], payload['password']):
        raise AccessForbiddenException(f'invalid password for user {payload["email"]}')
    now = datetime.now(ZoneInfo(os.getenv('TZ')))
    user_data = repo.get_user_data_by_email(payload["email"], ('id', 'name', 'lastname', ))
    payload = {**user_data,
               'exp': now + timedelta(hours=int(os.getenv('JWT_TIMEDELTA'))),
               'iat': now}
    token = jwt.encode(payload=payload, key=os.getenv('JWT_SECRET'),
                       algorithm="HS256")
    repo.store_last_valid_token(user_data['id'], token)
    return JSONResponse({'message': 'success',
                         'type': 'login_successful',
                         'detail': f'welcome back {user_data["name"]}!',
                         'user_data': {'authorization': f'Bearer {token}',
                                       **user_data}})


async def logout(request):
    repo = AuthRepository(request.state.engine)
    repo.delete_last_valid_token(request.state.current_user_id)
    return JSONResponse({'message': 'success',
                         'type': 'logout_successful',
                         'detail': 'see you later!'})


async def test(request):
    repo = AuthRepository(request.state.engine)
    user_data = repo.get_user_data_by_id(request.state.current_user_id, ('name', ))
    return JSONResponse({'message': 'success',
                         'type': 'test_successful',
                         'detail': f'route "{request.query_params["route"]}" reachable by user {user_data["name"]}'})


async def register(request):
    try:
        payload = await request.json()
    except json.JSONDecodeError as e:
        raise InvalidRequestBodyException(str(e))
    repo = AuthRepository(request.state.engine)
    repo.register_user(**payload)
    return JSONResponse({'message': 'success',
                         'type': 'successful_registration',
                         'detail': f'user {payload["name"]} created successfully'})
