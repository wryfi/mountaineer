from flask import abort
from sqlalchemy.orm import exc

from validators.uuid import uuid as valid_uuid

from mountaineer.app import db


def get_object_or_404(model, *criterion):
    """
    get_object_or_404 will retrieve a model from the database if it exists,
    otherwise it will abort the request with a 404 response.

    :param model: sqlalchemy model to query
    :param criterion: sqlalchemy filter expression
    :return: model instance or abort/404
    """
    try:
        return db.session.query(model).filter(*criterion).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)


def validate_uuid(func):
    """
    validate_uuid can be used as a decorator to validate that a function's
    id argument is a valid uuid.

    :param func: function to wrap
    :return: wrapped function
    """
    def wrapper(*args, **kwargs):
        try:
            if valid_uuid(kwargs['id']):
                return func(*args, **kwargs)
            else:
                return {'error': '{} is not a valid id'.format(kwargs['id'])}, 400
        except KeyError:
            return {'error': 'object has no id'}, 400
    return wrapper
