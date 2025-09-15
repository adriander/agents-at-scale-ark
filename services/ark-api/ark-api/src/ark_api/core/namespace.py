"""Namespace detection utilities."""
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Global variable to store the current namespace
_current_namespace: str = "default"


def is_namespace_detection_enabled() -> bool:
    """Check if namespace detection is enabled via environment variable."""
    env_value = os.getenv("ARK_DETECT_NAMESPACE", "false")
    enabled = env_value.lower() == "true"
    logger.info(f"ARK_DETECT_NAMESPACE={env_value}, namespace detection enabled: {enabled}")
    return enabled


def detect_current_namespace() -> str:
    """
    Detect the current namespace by reading the service account namespace file.
    Falls back to 'default' if the file is not found or cannot be read.
    If ARK_DETECT_NAMESPACE is false, always returns 'default'.
    """
    # If namespace detection is disabled, always return default
    if not is_namespace_detection_enabled():
        logger.info("Namespace detection disabled via ARK_DETECT_NAMESPACE, using default")
        return "default"

    namespace_file = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
    
    try:
        if namespace_file.exists():
            namespace = namespace_file.read_text().strip()
            logger.info(f"Detected current namespace from service account: {namespace}")
            return namespace
        else:
            logger.warning(f"Service account namespace file not found at {namespace_file}")
    except Exception as e:
        logger.warning(f"Failed to read service account namespace file: {e}")
    
    logger.info("Falling back to default namespace")
    return "default"


def set_current_namespace(namespace: str) -> None:
    """Set the current namespace."""
    global _current_namespace
    _current_namespace = namespace


def get_current_namespace() -> str:
    """Get the current namespace detected at startup."""
    return _current_namespace
