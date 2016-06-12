from pyramid.view import view_config


@view_config(context='smartgymapi.lib.factories.root.RootFactory',
             permission='public', renderer='json')
def root_view(request):
    return {'version': 1.01}
