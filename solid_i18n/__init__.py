import warnings
__author__ = 'st4lk'
__version__ = '1.4.0'

try:
    from django import VERSION
except ImportError:
    pass
else:
    DEPRECATED_DJANGO_VERSIONS = []

    if VERSION[:2] in DEPRECATED_DJANGO_VERSIONS:
        warnings.warn("Support of Django versions %s will be dropped soon"
            % DEPRECATED_DJANGO_VERSIONS, PendingDeprecationWarning)
