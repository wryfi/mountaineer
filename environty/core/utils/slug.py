import slugid

from django.core.exceptions import ObjectDoesNotExist


def replace_slug(anydict):
    """ Replace slug in anydict with decoded uuid

    :param dict anydict: a dictionary that might have a key named 'slug'
    :return: a dictionary where slug is replaced by the decoded uuid
    """
    if 'slug' in anydict.keys():
        try:
            anydict['uuid'] = slugid.decode(anydict['slug'])
        except ValueError as ex:
            raise ObjectDoesNotExist('could not match slug {} to any know object ({})'.format(anydict['slug'], ex))
        anydict.pop('slug')
    return anydict
