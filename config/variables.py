import environ
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


def required(key, default_value=None):
    try:
        value = env(key)
    except Exception:
        if not default_value:
            raise ImproperlyConfigured(f"Set the {key} environment variable")
        value = default_value
    return value


variables = {
    "django": {
        "secret_key": required("SECRET_KEY"),
    }
}
