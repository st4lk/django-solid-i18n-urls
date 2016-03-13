"""
Contains some code, copied from django, to support different versions of django.
"""
from django.utils.encoding import iri_to_uri
from django.utils.encoding import escape_uri_path


def get_full_path(request, force_append_slash=False):
    """
    Copied from django.http.request.get_full_path (django 1.9) to support
    older versions of django.
    """
    # RFC 3986 requires query string arguments to be in the ASCII range.
    # Rather than crash if this doesn't happen, we encode defensively.
    return '%s%s%s' % (
        escape_uri_path(request.path),
        '/' if force_append_slash and not request.path.endswith('/') else '',
        ('?' + iri_to_uri(request.META.get('QUERY_STRING', ''))) if request.META.get('QUERY_STRING', '') else ''
    )
