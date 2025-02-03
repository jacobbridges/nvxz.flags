class UsernameTakenError(Exception):
    """Raised when a username is taken."""


class ProjectNameTakenError(Exception):
    """Raised when a project name is already taken."""


class FlagNameTakenError:
    """Raised when a flag name is already taken."""
