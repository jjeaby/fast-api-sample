import datetime

from sqlalchemy import Column, String, Integer

from common.database.Connect import Base


class Links(Base):
    """
        Database Table Model
    """
    __tablename__ = "links"
    id = Column(Integer, autoincrement=False, primary_key=True)
    url = Column(String(255))
    name = Column(String(255))
    last_update = Column(String(255), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Links({self.id}, {self.url}, {self.name})>"

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
