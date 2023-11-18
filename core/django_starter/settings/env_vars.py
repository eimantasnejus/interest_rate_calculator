# globals() is a dictionary of global variables
from core.core.utils.collections import deep_update
from core.core.utils.settings import get_settings_from_environment

deep_update(globals(), get_settings_from_environment(ENV_VAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
