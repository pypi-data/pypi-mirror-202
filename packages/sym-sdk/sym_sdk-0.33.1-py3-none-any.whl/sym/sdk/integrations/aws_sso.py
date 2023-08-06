"""Helpers for interacting with the AWS SSO API within the Sym SDK."""

from sym.sdk.exceptions.aws import AWSSSOError  # noqa
from sym.sdk.user import User


def is_user_in_group(user: User, *, group_name: str) -> bool:
    """Checks if the provided :class:`~sym.sdk.user.User` is a member of the AWS SSO group specified.

    The AWS SSO group's display name must be given, and the method will check that the group exists and is
    accessible. An exception will be thrown if not.

    Args:
        user: The :class:`~sym.sdk.user.User` to check group membership of.
        group_name: The display name of the AWS SSO group.

    Returns:
        True if the :class:`~sym.sdk.user.User` is a member of the specified AWS SSO group, False otherwise.
    """
