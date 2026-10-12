from .settings import *  # noqa: F401,F403

# Used only when running tests. Never touches the real database.
SECRET_KEY = "test-secret-key-not-for-production"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Faster password hashing so the test suite runs quickly (test-only).
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]