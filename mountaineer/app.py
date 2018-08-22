import importlib
import os

import connexion
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy


mountaineer = connexion.FlaskApp(__name__)

mountaineer.app.config.from_object('mountaineer.defaults')
if 'MNTNR_SETTINGS_FILE' in os.environ.keys():
    mountaineer.app_config.from_envvar('MNTNR_SETTINGS_FILE')

for api in mountaineer.app.config['MOUNTAINEER_APIS']:
    module, version = api[0], api[1]
    spec = importlib.import_module(module + '.spec')
    mountaineer.add_api(spec.get_spec(version))

constraint_naming_convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=constraint_naming_convention)
db = SQLAlchemy(mountaineer.app, metadata=metadata)


if __name__ == '__main__':
    mountaineer.run(debug=True, port=8000)
