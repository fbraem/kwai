"""Module that defines value objects used with token entities."""

import ipaddress

from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from typing import Self


@dataclass(kw_only=True, frozen=True, slots=True)
class IpAddress:
    """An IP address."""

    ip: IPv4Address | IPv6Address

    def __str__(self) -> str:
        """Return string representation of an IP address."""
        return str(self.ip)

    @classmethod
    def create(cls, ip: str) -> Self:
        """Create an IpAddress instance from a string.

        A ValueError will be raised if the ip address is invalid.
        """
        return cls(ip=ipaddress.ip_address(ip))


@dataclass(kw_only=True, frozen=True, slots=True)
class OpenId:
    """OpenID information.

    sub: The subject identifier of the OpenID object.
    provider: The provider of the OpenID object.
    """

    sub: str
    provider: str
