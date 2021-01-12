"""
Configuration file for flask sample application
"""
import os

# enable CSRF
WTF_CSRF_ENABLED = True

# secret key for authentication
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "you-will-never-guess")

PYLTI_CONFIG = {
    "consumers": {
        "__consumer_key__": {
            "secret": os.environ.get("CONSUMER_KEY_SECRET", "__lti_secret__")
        }
    }
}
