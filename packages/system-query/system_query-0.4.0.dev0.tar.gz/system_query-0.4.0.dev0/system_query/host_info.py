"""Functions to query the host."""

import platform


def query_host() -> str:
    """Get information about current host."""
    hostname = platform.node()
    return hostname
