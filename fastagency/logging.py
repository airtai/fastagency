import logging

__all__ = ["get_logger"]


def get_logger(
    name: str, *, level: int = logging.INFO, use_timestamp: bool = True
) -> logging.Logger:
    """Return a logger with the specified name.

    Args:
        name (str): The name of the logger
        level (int): The level of the logger
        use_timestamp (bool): Whether to use a timestamp in the log messages
    """
    # Get the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Check if the logger already has handlers
    if not logger.handlers:
        # Create a stream handler
        handler = logging.StreamHandler()
        handler.setLevel(level)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter(
            f"{'%(asctime)s' if use_timestamp else ''} [%(levelname)s] %(message)s"
        )
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

    return logger
