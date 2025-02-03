class UsernameTakenError(Exception):
    """Raised when a username is taken."""
    pass


class ProjectNameTakenError(Exception):
    """Raised when a project name is already taken."""
    pass
