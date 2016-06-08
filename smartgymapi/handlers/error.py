import logging

from pyramid.view import forbidden_view_config, notfound_view_config

log = logging.getLogger(__name__)


@forbidden_view_config(renderer='json')
def forbidden(request):
    if not request.user:
        # No user logged in
        request.response.status_code = 401
        return {"message": "Unauthorized"}
    return {"message": "Forbidden"}


@notfound_view_config(renderer='json')
def notfound(request):
    return {"message": "Not found"}
