class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""
    pass


class EntityAlreadyExists(Exception):
    """Raised when a unique entity is already in database."""
    pass
