import os

import connexion
import yaml
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from mountaineer import utils


here = os.path.dirname(os.path.realpath(__file__))

constraint_naming_convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=constraint_naming_convention)
db = SQLAlchemy(metadata=metadata)


def create_app():
    mntnr = connexion.FlaskApp('mountaineer')

    mntnr.app.config.from_object('mountaineer.defaults')
    if 'MNTNR_SETTINGS_FILE' in os.environ.keys():
        mntnr.app_config.from_envvar('MNTNR_SETTINGS_FILE')

    api_version = mntnr.app.config['API_VERSION']
    base_specfile = os.path.join(here, 'api_{}'.format(api_version), 'openapi.yml')

    with open(base_specfile, 'rb') as spf:
        base_spec = yaml.safe_load(spf.read())

    api_spec = utils.assemble_api(mntnr.app.config['MOUNTAINEER_APIS'], base_spec)
    mntnr.add_api(api_spec)

    db.init_app(mntnr.app)

    return mntnr


def get_db():
    mntnr = create_app()
    mntnr.app.app_context().push()
    return db


if __name__ == '__main__':
    mountaineer = create_app()
    mountaineer.run(debug=True, port=8000)
