import logging
import sys

# Configure logging
logger = logging.getLogger("andrewaylett_pre_commit_hooks")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Create a separate error logger that outputs to stderr
error_logger = logging.getLogger("andrewaylett_pre_commit_hooks.error")
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setFormatter(formatter)
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)
error_logger.propagate = False  # Don't propagate to parent logger
