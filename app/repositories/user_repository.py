from app.repositories.base_repository import BaseRepository
from app.models.user_model import UserModel


class UserRepository(BaseRepository):
    model = UserModel

    @classmethod
    def get_by_name(cls, name):
        return cls.model.query.filter_by(name=name).first()

    @classmethod
    def delete_by_id(cls, id):
        user = cls.get_by_id(id)

        if user is None:
            return False

        cls.delete(user)

        return True
