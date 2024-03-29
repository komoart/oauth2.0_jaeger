from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from database.models import Users, AuthLogs
from core.utils import useragent_device_parser

db = SQLAlchemy()


def create_user_in_db(**kwargs):
    user = Users(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def update_user_in_db(user, **kwargs):
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
    return user


def get_user_or_404(**kwargs):
    return Users.query.filter_by(**kwargs).first_or_404()


def get_user(**kwargs):
    return Users.query.filter_by(**kwargs).first()


def update_history(user_agent, user_id):
    history = AuthLogs.query.filter_by(
        user_id=user_id,
        user_agent=user_agent).first()
    if not history:
        history = AuthLogs(
            user_id=user_id,
            user_agent=user_agent)
    history.updated_at = datetime.utcnow()
    ua = useragent_device_parser(user_agent)
    history.user_device_type = ua
    db.session.add(history)
    db.session.commit()


def get_auth_history_by_user_id(user_id, page, per_page):
    return AuthLogs.query.filter_by(
        user_id=user_id).paginate(page=page, per_page=per_page)


def add_role_to_user(user, role):
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        return True
    return False


def remove_role_from_user(user, role):
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return True
    return False
