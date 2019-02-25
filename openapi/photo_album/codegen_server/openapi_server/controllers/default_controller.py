import time
import uuid

import connexion
import six

from openapi_server.helpers import local as helper
from openapi_server.models.error_message import ErrorMessage  # noqa: E501
from openapi_server.models.inline_response200 import InlineResponse200 #noqa: E501
from openapi_server.models.photo import Photo  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server import util

API_SERVICE_NAME = '//photos.myapiservice.com'

PAGE_SIZE = 10

def add_photo(user_id, data, name=None, create_time=None):  # noqa: E501
    """add_photo

    Adds a photo # noqa: E501

    :param user_id: ID of user
    :type user_id: str
    :param data: 
    :type data: str
    :param name: 
    :type name: str
    :param create_time: 
    :type create_time: int

    :rtype: Photo
    """
    parent = '{}/users/{}'.format(API_SERVICE_NAME, user_id)
    photo_id = uuid.uuid4().hex
    name = '{}/users/{}/photos/{}'.format(API_SERVICE_NAME, user_id, photo_id)
    photo = Photo(
        name=name,
        created_at=int(time.time()),
        data=data
    )

    try:
        helper.create_photo(parent, photo)
    except ValueError:
        return ErrorMessage(
            error_code='404 NOT_FOUND',
            error_message='NOT_FOUND: Cannot find specified user.'
        )
    return photo


def batchget_photo(user_id, photo_ids):  # noqa: E501
    """batchget_photo

    Gets a list of photos # noqa: E501

    :param user_id: ID of user
    :type user_id: str
    :param photo_ids: a collection of photo IDs
    :type photo_ids: List[str]

    :rtype: List[Photo]
    """
    res = []
    for photo_id in photo_ids:
        res.append(get_photo(user_id))
    return res


def create_user(user=None):  # noqa: E501
    """create_user

    Creates a new user # noqa: E501

    :param user: The user to create
    :type user: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    
    user_id = uuid.uuid4().hex
    name = '{}/users/{}'.format(API_SERVICE_NAME, user_id)
    user.name = name

    helper.create_user(name, user)
    return user

def delete_photo(user_id, photo_id):  # noqa: E501
    """delete_photo

    Deletes a photo # noqa: E501

    :param user_id: ID of user
    :type user_id: str
    :param photo_id: ID of photo
    :type photo_id: str

    :rtype: None
    """
    name = '{}/users/{}/photos/{}'.format(API_SERVICE_NAME, user_id, photo_id)

    try:
        helper.delete_photo(name)
    except ValueError:
        return ErrorMessage(
            error_code='404 NOT_FOUND',
            error_message='NOT_FOUND: Cannot find specifed photo.'
        )

    return


def get_photo(user_id, photo_id):  # noqa: E501
    """get_photo

    Gets a photo # noqa: E501

    :param user_id: ID of user
    :type user_id: str
    :param photo_id: ID of photo
    :type photo_id: str

    :rtype: Photo
    """
    name = '{}/users/{}/photos/{}'.format(API_SERVICE_NAME, user_id, photo_id)

    photo = helper.get_photo(name)
    if not photo:
        return ErrorMessage(
            error_code='404 NOT_FOUND',
            error_message='NOT_FOUND: Cannot find specified photo.'
        )

    return photo


def get_user(user_id):  # noqa: E501
    """get_user

    Gets a user # noqa: E501

    :param user_id: ID of user
    :type user_id: str

    :rtype: User
    """
    name = '{}/users/{}'.format(API_SERVICE_NAME, user_id)
    user = helper.get_user(name)

    if not user:
        return ErrorMessage(
            error_code='404 NOT_FOUND',
            error_message='NOT_FOUND: Cannot find specified user.'
        )

    return user


def list_photos(user_id, order_by=None, page_token=None):  # noqa: E501
    """list_photos

    Lists all photos # noqa: E501

    :param user_id: ID of user
    :type user_id: str
    :param order_by: Ordering for the results
    :type order_by: str
    :param page_token: Token for the next page
    :type page_token: str

    :rtype: InlineResponse200
    """
    if page_token:
        token_context = helper.get_token_context(page_token)
        if not token_context:
            return ErrorMessage(
                error_code='404 NOT_FOUND',
                error_message='NOT_FOUND: Cannot find specified page token.'
            )
    else:
        token_context = {
            'parent': '{}/users/{}'.format(API_SERVICE_NAME, user_id),
            'order_by': order_by,
            'offset': 0,
            'page_size': PAGE_SIZE
        }
    
    try:
        photos, if_has_more_photos = helper.list_photos(**token_context)
    except ValueError:
        return ErrorMessage(
            error_code='404 NOT_FOUND',
            error_message='NOT_FOUND: Cannot find specified user.'
        )

    # Prepare a new token if there are more photos
    next_page_token = None
    if if_has_more_photos:
        next_page_token = uuid.uuid4().hex
        token_context['offset'] += token_context['page_size']
        helper.add_token_context(next_page_token, token_context)

    return InlineResponse200(photos=photos, next_page_token=next_page_token)


def update_user(user_id, user=None):  # noqa: E501
    """update_user

    Updates a user # noqa: E501

    :param user_id: ID of user
    :type user_id: str
    :param user: The user to update
    :type user: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    
    name = '{}/users/{}'.format(API_SERVICE_NAME, user_id)
    user.name = name
    
    if not helper.get_user(name):
        return ErrorMessage(
            error_code='404 NOT_FOUND',
            error_message='NOT_FOUND: Cannot find specified user.'
        )

    helper.update_user(name, user)

    return user
