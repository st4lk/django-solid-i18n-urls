import warnings
__author__ = 'st4lk'
__version__ = '1.1.1'

try:
    from django import VERSION
except ImportError:
    pass
else:
    DEPRECATED_DJANGO_VERSIONS = [(1, 4), (1, 5), (1, 6), (1, 7)]

    if VERSION[:2] in DEPRECATED_DJANGO_VERSIONS:
        warnings.warn("Support of Django versions %s will be dropped soon"
            % DEPRECATED_DJANGO_VERSIONS, PendingDeprecationWarning)
