import bcrypt
from sqlalchemy.orm import\
    Session
from ..models.user import\
    User
from sqlalchemy import\
    select


class AuthRepository:
    def __init__(self, engine):
        self._engine = engine

    def is_token_valid(self, id, token):
        res = False
        with Session(self._engine) as session:
            user = session.scalars(select(User).where(User.id == id)).one()
            res = user.last_valid_token == token
        return res

    def is_password_valid(self, email, payload_password):
        res = False
        with Session(self._engine) as session:
            user = session.scalars(select(User).where(User.email == email)).one()
            hashed_password = bytes(user.password.encode('utf-8'))
            password = bytes(payload_password.encode('utf-8'))
            res = bcrypt.checkpw(password, hashed_password)
        return res

    def store_last_valid_token(self, user_id, token):
        with Session(self._engine) as session:
            try:
                user = session.scalars(select(User).where(User.id == user_id)).one()
                user.last_valid_token = token
                session.add(user)
                session.flush()
            except Exception as e:
                session.rollback()
                raise e
            else:
                session.commit()

    def delete_last_valid_token(self, user_id):
        with Session(self._engine) as session:
            try:
                user = session.scalars(select(User).where(User.id == user_id)).one()
                user.last_valid_token = None
                session.add(user)
                session.flush()
            except Exception as e:
                session.rollback()
                raise e
            else:
                session.commit()

    def register_user(self, *, password, email, name, lastname):
        id = None
        with Session(self._engine) as session:
            try:
                hashed_password = bcrypt.hashpw(bytes(password.encode('utf-8')),
                                                bcrypt.gensalt(rounds=15))
                new_user = User(**{'password': hashed_password.decode('utf-8'),
                                   'email': email, 'name': name, 'lastname': lastname})
                session.add(new_user)
                session.flush()
                id = new_user.id
            except Exception as e:
                session.rollback()
                raise e
            else:
                session.commit()
        return id

    def get_user_data(self, email, data):
        res = {}
        with Session(self._engine) as session:
            user = session.scalars(select(User).where(User.email == email)).one()
            for d in data:
                res[d] = getattr(user, d, None)
        return res
