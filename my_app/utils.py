from urllib.parse import urlparse, urlunparse


def is_safe_url(url, allowed_hosts=None, require_https=False):
    """
    Return ``True`` if the url is a safe redirection (i.e. it doesn't point to
    a different host and uses a safe scheme).
    """
    try:
        url_info = urlparse(url)
    except ValueError:
        return False
    # If not a valid URL, fail fast
    if not url_info.scheme or not url_info.netloc:
        return False
    # Don't allow redirects to different hosts unless explicitly allowed
    if allowed_hosts is not None:
        # Ensure that we don't get false matches due to subdomains
        # by comparing the canonical domains
        host = url_info.hostname
        if host not in allowed_hosts:
            if not any(host.endswith('.' + domain) for domain in allowed_hosts):
                return False
    # If HTTPS is required, check that the scheme is HTTPS
    if require_https and url_info.scheme != 'https':
        return False
    # Check that the URL is not an absolute URI
    if url_info.scheme in ['http', 'https']:
        return not url_info.path.startswith('//')
    # Check that the URL is a relative path
    return not bool(urlparse(url_info.path).netloc)
