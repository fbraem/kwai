"""Module that defines a recipient."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.email_address import EmailAddress


@dataclass(kw_only=True, frozen=True)
class Recipient:
    """Defines a recipient."""

    email: EmailAddress
    name: str


@dataclass(frozen=True)
class Recipients:
    """Defines all recipients for an email."""

    from_: Recipient
    to: list[Recipient] = field(default_factory=list)
    cc: list[Recipient] = field(default_factory=list)
    bcc: list[Recipient] = field(default_factory=list)

    def with_from(self, from_) -> "Recipients":
        return Recipients(from_, self.to, self.cc, self.bcc)

    def with_to(self, *to: Recipient) -> "Recipients":
        return Recipients(self.from_, list(to), self.cc, self.bcc)

    def add_to(self, *to: Recipient) -> "Recipients":
        return Recipients(self.from_, self.to + list(to), self.cc, self.bcc)

    def with_cc(self, *cc: Recipient) -> "Recipients":
        return Recipients(self.from_, self.to, list(cc), self.bcc)

    def add_cc(self, *cc: Recipient) -> "Recipients":
        return Recipients(self.from_, self.to, self.cc + list(cc), self.bcc)

    def with_bcc(self, *bcc: Recipient) -> "Recipients":
        return Recipients(self.from_, self.to, self.cc, list(bcc))

    def add_bcc(self, *bcc: Recipient) -> "Recipients":
        return Recipients(self.from_, self.to, self.cc, self.bcc + list(bcc))
