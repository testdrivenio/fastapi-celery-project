import factory
from factory import LazyAttribute
from factory.fuzzy import FuzzyText

from project.database import SessionLocal
from project.users.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = SessionLocal()
        sqlalchemy_get_or_create = ("username",)
        sqlalchemy_session_persistence = "commit"

    username = FuzzyText(length=6)
    email = LazyAttribute(lambda o: "%s@example.com" % o.username)
