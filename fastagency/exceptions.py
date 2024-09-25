class FastAgencyError(Exception):
    pass


class FastAgencyCLIError(FastAgencyError):
    pass


class FastAgencyCLIPythonVersionError(FastAgencyCLIError):
    pass
