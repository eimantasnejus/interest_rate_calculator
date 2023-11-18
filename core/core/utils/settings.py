import os

from core.core.utils.misc import yaml_coerce


def get_settings_from_environment(prefix):
    """Get settings from environment variables.

    sample:
    'DOCKERSETTINGS_DATABASE_HOST=postgres' -> {'DATABASE_HOST': 'postgres'}
    """
    prefix_length = len(prefix)
    return {key[prefix_length:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)}
