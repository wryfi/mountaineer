from flask_sqlalchemy import Model


class BaseModel(Model):
    def serialize(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
