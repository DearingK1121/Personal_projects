import ipaddress
import re


def analyze_input(value: str) -> dict:
    """Analyze an IP address string and classify it.

    Returns a dictionary with:
    - kind: 'ipv4' or 'ipv6'
    - is_public: True for globally routable public addresses
    - category: one of private, loopback, link-local, documentation,
      reserved, global, or unspecified
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Input must be a non-empty string")

    try:
        addr = ipaddress.ip_address(value.strip())
    except ValueError as exc:
        raise ValueError(f"Invalid IP address: {value}") from exc

    if isinstance(addr, ipaddress.IPv4Address):
        kind = "ipv4"
    else:
        kind = "ipv6"

    if addr.is_loopback:
        category = "loopback"
    elif isinstance(addr, ipaddress.IPv6Address) and addr in ipaddress.IPv6Network("2001:db8::/32"):
        category = "documentation"
    elif addr.is_private:
        category = "private"
    elif addr.is_link_local:
        category = "link-local"
    elif addr.is_reserved:
        category = "reserved"
    elif addr.is_multicast:
        category = "multicast"
    elif addr.is_unspecified:
        category = "unspecified"
    elif addr.is_global:
        category = "global"
    else:
        category = "unknown"

    return {
        "kind": kind,
        "is_public": addr.is_global,
        "category": category,
    }


def find_ip_addresses(text: str) -> list[str]:
    """Extract valid IP addresses from a string."""
    if not isinstance(text, str) or not text.strip():
        return []

    pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:[0-9A-Fa-f]{0,4}:){1,7}[0-9A-Fa-f]{0,4}\b")
    candidates = pattern.findall(text)
    results = []

    for candidate in candidates:
        try:
            ipaddress.ip_address(candidate)
        except ValueError:
            continue
        results.append(candidate)

    return results
