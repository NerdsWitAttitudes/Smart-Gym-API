def update_playlist(request):
    settings = request.registry.settings
    client_id = settings['spotify.client.id']
    client_secret = settings['spotify.client.secret']
    base_url = settings['spotify.base_url']

    return
