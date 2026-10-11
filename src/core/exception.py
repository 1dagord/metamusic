class NoMetadataAvailableError(Exception):
    """
    Throw when an operation is attempted on metadata that has not yet been read or stored
    """