"""
Contains some code, copied from django, to support different versions of django.
"""
from django.utils.encoding import iri_to_uri, force_bytes
try:
    from django.utils.six.moves.urllib.parse import quote
except ImportError:
    from urllib import quote
try:
    from django.utils.encoding import escape_uri_path
except ImportError:

    def escape_uri_path(path):
        """
        Escape the unsafe characters from the path portion of a Uniform Resource
        Identifier (URI).
        """
        # These are the "reserved" and "unreserved" characters specified in
        # sections 2.2 and 2.3 of RFC 2396:
        #   reserved    = ";" | "/" | "?" | ":" | "@" | "&" | "=" | "+" | "$" | ","
        #   unreserved  = alphanum | mark
        #   mark        = "-" | "_" | "." | "!" | "~" | "*" | "'" | "(" | ")"
        # The list of safe characters here is constructed subtracting ";", "=",
        # and "?" according to section 3.3 of RFC 2396.
        # The reason for not subtracting and escaping "/" is that we are escaping
        # the entire path, not a path segment.
        return quote(force_bytes(path), safe=b"/:@&+$,-_.!~*'()")


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
