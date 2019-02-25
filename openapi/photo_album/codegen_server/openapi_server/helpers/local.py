users = {}
photos = {}
tokens = {}

PAGE_SIZE = 10

def create_user(name, user):
    users[name] = user

def update_user(name, user):
    users[name] = user

def delete_user(name):
    pass

def get_user(name):
    return users.get(name)

def create_photo(parent, photo):
    user = users.get(parent)
    if not user:
        raise ValueError('Parent not found.')
    photo_library = photos.get(parent, [])
    photo_library.append(photo)
    photos[parent] = photo_library

def upload_photo(name, data):
    pass

def list_photos(parent, order_by, offset, page_size):
    user = users.get(parent)
    if not user:
        raise ValueError('Parent not found.')
    photo_library = photos.get(parent, [])

    return sort_photos(photo_library, order_by, offset, page_size)

def sort_photos(photo_library, order_by, offset, page_size):
    if order_by == 'created_at':
        sorted_photos = sorted(photo_library, key=lambda x:x.created_at)
    else:
        sorted_photos = sorted(photo_library, key=lambda x:x.display_name)
    
    if_has_more_photos = True
    if len(photo_library) < offset + page_size:
        if_has_more_photos = False

    return sorted_photos[offset:offset + page_size], if_has_more_photos
    
def delete_photo(name):
    parent = name.split('/photos')[0]
    photo_library = photos.get(parent, [])
    for i in range(0, len(photo_library)):
        if photo_library[i].name == name:
            photo_library.pop(i)
            return
    
    raise ValueError

def get_photo(name):
    parent = name.split('/photos')[0]
    photo_library = photos.get(parent, [])
    for photo in photo_library:
        if photo.name == name:
            return photo

def get_token_context(token):
    return tokens.get(token)

def add_token_context(token, context):
    tokens[token] = context
