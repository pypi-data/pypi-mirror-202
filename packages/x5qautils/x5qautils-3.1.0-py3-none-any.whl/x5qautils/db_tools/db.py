import logging
import textwrap

import allure


def close_pg(pp):
    pp['s'].close_all()
    pp['conn'].close()


def log_db(func):
    def wrapper(*args, **kwargs):
        logging.info('Get last db entity with param')
        result = func(*args, kwargs)
        logging.info('Entity is getted: %s', textwrap.shorten(str(result), 200))
        return result

    return wrapper


@allure.step("Получить запись из таблицы по id")
@log_db
def get_entity_by_id_one(session, cls, id_):
    return session.query(cls).filter(cls.id == id_).all()


@allure.step("Получить последнюю запись из таблицы")
@log_db
def get_last_entity(session, cls, field, **kwargs):
    return session.query(cls).filter_by(**kwargs).order_by(field.desc()).first()


@allure.step("Получить последнюю запись из таблицы")
@log_db
def get_last_n_entity(session, cls, n, field, order='asc', **kwargs):
    return session.query(cls).filter_by(**kwargs).order_by(getattr(field, order)()).limit(n).all()  # noqa: ECE001


@allure.title('Get entities with custom filters')
@log_db
def get_entity_by_params(session, cls, **kwargs):
    return session.query(cls).filter_by(**kwargs).first()


@allure.title('Получить сущности из бд с кастомным фильтром')
@log_db
def get_entities_by_params(session, cls, **kwargs):
    return session.query(cls).filter_by(**kwargs).all()


@allure.title('Get entities with custom filters and regexp filter')
@log_db
def entities_with_regexp(session, cls, param, param_value, **kwargs):
    return session.query(cls).filter_by(**kwargs).filter(param.like(param_value)).all()


@allure.title('Get entities with custom filters and regexp filter')
@log_db
def entity_with_regexp(session, cls, param, param_value, field, **kwargs):
    return session.query(cls).filter_by(**kwargs).filter(param.like(param_value)).order_by(field.desc()).first()  # noqa


@allure.title('Get entities with custom filters and regexp filter')
@log_db
def last_entity_with_only_regexp(session, cls, param, param_value, field, **kwargs):
    return session.query(cls).filter_by(**kwargs).filter(param.like(param_value)).order_by(field.desc()).first()  # noqa
