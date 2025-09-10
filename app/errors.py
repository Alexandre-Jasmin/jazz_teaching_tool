class ServiceError(Exception):
    """Base service error for all service-related issues."""
    pass

class SummonerNotFound(ServiceError):
    """Raised when a summoner could not be found."""
    pass

class MatchNotFound(ServiceError):
    """Raised when a match could not be found."""
    pass
