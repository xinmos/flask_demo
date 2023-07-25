from model.user import User


class UserService(object):
    @staticmethod
    def query_by_id(user_id: int) -> dict:
        user = User.query.filter_by(id=user_id).first()
        return user.to_dict()
