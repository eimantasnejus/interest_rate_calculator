import os
from pathlib import Path

from split_settings.tools import include, optional

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespacing our own custom environment variables
ENV_VAR_SETTINGS_PREFIX = "CORE_SETTINGS_"

LOCAL_SETTINGS_PATH = os.getenv(f"{ENV_VAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = os.path.join(BASE_DIR, LOCAL_SETTINGS_PATH)

include(
    "base.py",
    "logging.py",
    "custom.py",
    optional(LOCAL_SETTINGS_PATH),
    "env_vars.py",
    "docker.py",
)
