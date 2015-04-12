import warnings
__author__ = 'st4lk'
__version__ = '0.9.1'

try:
    from django import VERSION
except ImportError:
    pass
else:
    DEPRECATED_DJANGO_VERSIONS = [(1, 5)]

    if VERSION[:2] in DEPRECATED_DJANGO_VERSIONS:
        warnings.warn("Support of Django versions %s will be dropped in "
            "1.0 version of solid_i18n" % DEPRECATED_DJANGO_VERSIONS,
            PendingDeprecationWarning)
