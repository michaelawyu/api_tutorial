import connexion
import six

from openapi_server.models.error_message import ErrorMessage  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server import util


def get_user(user_id):  # noqa: E501
    """get_user

    Gets an user # noqa: E501

    :param user_id: ID of a user
    :type user_id: str

    :rtype: User
    """
    user = User(
        name=user_id,
        display_name='Example User',
        email='user@example.com'
    )
    return user
