"""
Logging utilities for the code similarity detection system.

This module provides centralized logging configuration and utilities
to ensure consistent logging across all modules.
"""

import logging
import sys
from typing import Optional


# Default log level mappings
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    log_file: Optional[str] = None,
    console: bool = True
) -> None:
    """
    Configure logging for the entire application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        log_file: Optional file path to write logs to
        console: Whether to output logs to console (default True)
    
    Raises:
        ValueError: If level is invalid
    """
    if level.upper() not in LOG_LEVELS:
        raise ValueError(
            f"Invalid log level '{level}'. Must be one of: {list(LOG_LEVELS.keys())}"
        )
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVELS[level.upper()])
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Default format
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, IOError) as e:
            # Fallback to console if file logging fails
            logger.warning(f"Could not create log file '{log_file}': {e}")
    
    # Log the setup
    logger.info(f"Logging configured: level={level}, console={console}, file={log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """
    Change the logging level at runtime.
    
    Args:
        level: New logging level
    
    Raises:
        ValueError: If level is invalid
    """
    if level.upper() not in LOG_LEVELS:
        raise ValueError(
            f"Invalid log level '{level}'. Must be one of: {list(LOG_LEVELS.keys())}"
        )
    
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVELS[level.upper()])
    logger.info(f"Log level changed to {level}")


# Convenience functions for common log levels
def debug(message: str, *args, **kwargs) -> None:
    """Log a debug message."""
    logging.debug(message, *args, **kwargs)


def info(message: str, *args, **kwargs) -> None:
    """Log an info message."""
    logging.info(message, *args, **kwargs)


def warning(message: str, *args, **kwargs) -> None:
    """Log a warning message."""
    logging.warning(message, *args, **kwargs)


def error(message: str, *args, **kwargs) -> None:
    """Log an error message."""
    logging.error(message, *args, **kwargs)


def critical(message: str, *args, **kwargs) -> None:
    """Log a critical message."""
    logging.critical(message, *args, **kwargs)


# Initialize with default settings when module is imported
# This ensures logging works even if setup_logging() is not called
if not logging.getLogger().hasHandlers():
    setup_logging(level="INFO")