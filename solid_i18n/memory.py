from threading import local

_language_from_path = local()


def set_language_from_path(language):
    _language_from_path.value = language


def get_language_from_path():
    return getattr(_language_from_path, 'value', None)
