"""Namespace and context detection utilities."""
import logging
from ark_sdk.k8s import get_context

logger = logging.getLogger(__name__)

# Global variable to store the current context
_current_context: dict = {"namespace": "default", "cluster": "unknown"}


def detect_current_context() -> dict:
    """
    Detect the current Kubernetes context using ark-sdk.
    
    Uses standard k8s patterns:
    1. In-cluster service account (when running in pods)
    2. Kubeconfig context (when running locally)
    3. Fallback to default
    
    Returns:
        dict: Context with 'namespace' and 'cluster' keys
    """
    try:
        context = get_context()
        logger.info(f"Detected context: namespace={context['namespace']}, cluster={context['cluster']}")
        return context
    except Exception as e:
        logger.warning(f"Failed to detect context: {e}")
        fallback = {"namespace": "default", "cluster": "unknown"}
        logger.info(f"Using fallback context: {fallback}")
        return fallback


def set_current_context(context: dict) -> None:
    """Set the current context."""
    global _current_context
    _current_context = context


def get_current_context() -> dict:
    """Get the current context detected at startup."""
    return _current_context
