SQLALCHEMY_DATABASE_URI = 'postgres://mntnr_flask:mntnr_flask@localhost/mntnr_flask'
SQLALCHEMY_TRACK_MODIFICATIONS = False

API_VERSION = 'v1'

MOUNTAINEER_APIS = [
    ('mntnr_hardware', API_VERSION),
]