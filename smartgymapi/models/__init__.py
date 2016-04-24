import transaction
from smartgymapi.models.meta import DBSession as session


def commit():
    transaction.commit()


def persist(obj):
    session.add(obj)


def delete(obj):
    session.delete(obj)


def rollback():
    return session.rollback()
