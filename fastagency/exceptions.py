class FastAgencyError(Exception):
    pass


class FastAgencyCLIError(FastAgencyError):
    pass


class FastAgencyCLIPythonVersionError(FastAgencyCLIError):
    pass


class FastAgencyWSGINotImplementedError(FastAgencyError):
    pass


class FastAgencyASGINotImplementedError(FastAgencyError):
    pass


class FastAgencyConnectionError(FastAgencyError):
    pass


class FastAgencyNATSConnectionError(FastAgencyConnectionError):
    pass


class FastAgencyFastAPIConnectionError(FastAgencyConnectionError):
    pass


class FastAgencyKeyError(KeyError):
    pass


class FastAgencyNATSKeyError(FastAgencyKeyError):
    pass


class FastAgencyFastAPIKeyError(FastAgencyKeyError):
    pass
