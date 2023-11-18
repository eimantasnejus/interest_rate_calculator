DEBUG = True
SECRET_KEY = "django-insecure-q%)qq+7($2wrrp_@&bmhd68^t9pu0s3bhjdn33_*h_ntq2()l&"

LOGGING["formatters"]["colored"] = {  # type: ignore  # noqa: F821
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}
LOGGING["loggers"]["cooking_core"]["level"] = "DEBUG"  # type: ignore  # noqa: F821
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore  # noqa: F821
LOGGING["handlers"]["console"]["formatter"] = "colored"  # type: ignore  # noqa: F821
