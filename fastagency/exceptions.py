class FastAgencyError(Exception):
    pass


class FastAgencyValueError(ValueError):
    pass


class FastAgencyCLIError(FastAgencyError):
    pass


class FastAgencyCLIPythonVersionError(FastAgencyCLIError):
    pass


class FastAgencyWSGINotImplementedError(FastAgencyError):
    pass


class FastAgencyASGINotImplementedError(FastAgencyError):
    pass


class FastAgencyNATSConnectionError(FastAgencyValueError):
    pass


class FastAgencyFastAPIConnectionError(FastAgencyValueError):
    pass
