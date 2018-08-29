import importlib
import os

from deepmerge import always_merger
import connexion
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
import yaml

from mountaineer.database import BaseModel


here = os.path.dirname(os.path.realpath(__file__))

constraint_naming_convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=constraint_naming_convention)
db = SQLAlchemy(metadata=metadata, model_class=BaseModel)


def assemble_api(mntnr_apis, base_spec):
    api_spec = {}
    for api in mntnr_apis:
        module, version = api[0], api[1]
        spec = importlib.import_module(module + '.spec')
        api_spec = always_merger.merge(api_spec, spec.get_spec(version))
    return always_merger.merge(api_spec, base_spec)


def import_format_checks(mntnr_apis):
    """
    import_format_checks is used in initializing the application. Custom field
    types for Connexion/OpenAPI must be registered before the application is
    started. This function is used to gather and import them all.

    :param mntnr_apis: list of mountaineer APIs, from settings
    :return: None
    """
    from mountaineer import format_checks
    for api in mntnr_apis:
        module = api[0]
        import_statement = 'from {} import format_checks'.format(module)
        try:
            exec(import_statement)
        except ImportError:
            pass


def create_app():
    mntnr = connexion.FlaskApp('mountaineer')

    mntnr.app.config.from_object('mountaineer.defaults')
    if 'MNTNR_SETTINGS_FILE' in os.environ.keys():
        mntnr.app_config.from_envvar('MNTNR_SETTINGS_FILE')

    api_version = mntnr.app.config['API_VERSION']
    base_specfile = os.path.join(here, 'api_{}'.format(api_version), 'openapi.yml')

    with open(base_specfile, 'rb') as spf:
        base_spec = yaml.safe_load(spf.read())

    import_format_checks(mntnr.app.config['MOUNTAINEER_APIS'])

    api_spec = assemble_api(mntnr.app.config['MOUNTAINEER_APIS'], base_spec)
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
