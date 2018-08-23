from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy


constraint_naming_convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=constraint_naming_convention)
db = SQLAlchemy(metadata=metadata)


def get_db():
    from mountaineer.app import create_app
    app = create_app()
    db.init_app(app.app)
    return db
