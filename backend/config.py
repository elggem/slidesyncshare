"""
Configuration file for flask sample application
"""
import os

# enable CSRF
WTF_CSRF_ENABLED = True

# secret key for authentication
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "you-will-never-guess")

CONSUMER_KEY_PEM_FILE = os.path.abspath('consumer_key.pem')
with open(CONSUMER_KEY_PEM_FILE, 'w') as wfile:
    wfile.write(os.environ.get('CONSUMER_KEY_CERT', ''))

PYLTI_CONFIG = {
    "consumers": {
        "__consumer_key__": {
            "secret": os.environ.get("CONSUMER_KEY_SECRET", "__lti_secret__"),
            "cert": CONSUMER_KEY_PEM_FILE
        }
    }
}
