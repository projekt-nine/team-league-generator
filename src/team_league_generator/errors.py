class NotIterableError(Exception):
    pass


class InvalidSizeRequestError(Exception):
    pass


class KeywordError(Exception):
    pass


class GeographyError(Exception):
    pass


class CountryCodeError(GeographyError):
    pass
