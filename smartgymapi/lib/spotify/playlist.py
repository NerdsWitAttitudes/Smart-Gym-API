import logging

from smartgymapi.models.user import list_current_users_in_gym

log = logging.getLogger(__name__)


def update_playlist(request, gym_id):
    settings = request.registry.settings
    client_id = settings['spotify.client.id']
    client_secret = settings['spotify.client.secret']
    base_url = settings['spotify.base_url']

    users_in_gym = (list_current_users_in_gym(gym_id))
    for user in users_in_gym:
        log.info(user)
    return
