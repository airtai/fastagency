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
