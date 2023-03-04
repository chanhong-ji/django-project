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
        "secret_key": required("DJANGO_SECRET_KEY"),
    },
    "cors": {
        "domain": required("CORS_DOMAIN"),
    },
    "github": {
        "client_id": required("GH_CLIENT"),
        "client_secret": required("GH_SECRET"),
    },
    "kakao": {
        "client_id": required("KA_CLIENT"),
        "client_secret": required("KA_SECRET"),
        "redirect_url": required("KAKAO_REDIRECT_URL"),
    },
    "cf": {
        "client_id": required("CF_ACCOUNT_ID"),
        "client_token": required("CF_TOKEN"),
    },
    "deploy": {
        "mode": required("HEROKU_IS", "False"),
        "host_url": required("HOST_URL", "*"),
    },
}
