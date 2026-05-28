from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def create_user(name):
        existing_user = UserRepository.get_by_name(name)

        if existing_user:
            raise Exception("User already exists")

        return UserRepository.create(name=name)

    @staticmethod
    def delete_user(id):
        if UserRepository.delete_by_id(id):
            return True
        else:
            raise Exception("User not deleted")
