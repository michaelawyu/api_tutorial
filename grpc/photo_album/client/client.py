import hashlib
import uuid

from google.protobuf import field_mask_pb2
import grpc

from codegen import example_pb2
from codegen import example_pb2_grpc

SERVER_ADDRESS = '0.0.0.0'
PORT = 8080
BLOCK_SIZE = 20000

class PhotoDataBlockRequestIterable(object):
    def __init__(self, name, photo_path):
        self.name = name
        self.photo_path = photo_path
        
        with open(photo_path, 'rb') as f:
            self.data = f.read()
        self.data_hash = hashlib.new('md5', self.data).hexdigest()
        self.loc = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        data_block = self.data[self.loc:self.loc + BLOCK_SIZE]
        if data_block:
            data_block_hash = hashlib.new('md5', data_block).hexdigest()
            request = example_pb2.PhotoDataBlock(
                name = self.name,
                data_block = data_block,
                data_block_hash = data_block_hash,
                data_hash = self.data_hash
            )
            self.loc += BLOCK_SIZE
            return request
        else:
            raise StopIteration

class ListPhotosResponseIterable(object):
    def __init__(self, stub, initial_response):
        self.stub = stub
        self.initial_response = initial_response
        self.if_initial_response_returned = False
        self.next_page_token = initial_response.next_page_token
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.if_initial_response_returned:
            self.if_initial_response_returned = True
            return self.initial_response.photos
        
        if self.next_page_token:
            request = example_pb2.ListPhotosRequest(
                page_token = self.next_page_token
            )
            try:
                response = self.stub.ListPhotos(request)
                self.next_page_token = response.next_page_token
                return response.photos
            except grpc.RpcError as err:
                print(err.details()) #pylint: disable=no-member
                print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member
        else:
            raise StopIteration

class ExamplePhotoServiceClient(object):
    def __init__(self):
        """Initializer. 
           Creates a gRPC channel for connecting to the server.
           Adds the channel to the generated client stub.
        Arguments:
            None.
        
        Returns:
            None.
        """
        self.channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{PORT}')
        self.stub = example_pb2_grpc.ExamplePhotoServiceStub(self.channel)

    def create_user(self, display_name, email):
        """Creates a user.

        Arguments:
            display_name: The display name of a user.
            email: The email of a user.
        
        Returns:
            None; outputs to the terminal.
        """
        request = example_pb2.User(
            display_name=display_name,
            email=email
        )

        try:
            response = self.stub.CreateUser(request)
            print('User created.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member

    def get_user(self, name):
        request = example_pb2.GetUserRequest(
            name = name
        )

        try:
            response = self.stub.GetUser(request)
            print('User fetched.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member

    def update_user(self, name, display_name = None, email = None):
        """Updates a user.

        Arguments:
            display_name: The display name of a user.
            email: The email of a user.
        
        Returns:
            None; outputs to the terminal.
        """
        mask = field_mask_pb2.FieldMask()
        
        if display_name:
            mask.paths.append('display_name') #pylint: disable=no-member
        if email:
            mask.paths.append('email') #pylint: disable=no-member
        if not mask.paths: #pylint: disable=no-member
            raise ValueError('There are no attributes to update.')

        request = example_pb2.UpdateUserRequest(
            name = name,
            user = example_pb2.User(
                display_name=display_name,
                email=email
            ),
            mask = mask
        )

        try:
            response = self.stub.UpdateUser(request)
            print('User updated.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member
    
    def create_photo(self, parent, display_name):
        """Creates a photo.

        Arguments:
            parent: The resource name of a user.
            display_name: The display name of a photo.
        
        Returns:
            None; outputs to the terminal.
        """
        request = example_pb2.CreatePhotoRequest(
            parent=parent,
            photo=example_pb2.Photo(
                display_name=display_name
            )
        )

        try:
            response = self.stub.CreatePhoto(request)
            print('Photo created.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value())) #pylint: disable=no-member
    
    def upload_photo(self, name, photo_path):
        """Uploads a photo.

        Arguments:
            name: The resource name of a photo.
            photo_path: The path to a binary image file.
        
        Returns:
            None; outputs to the terminal.
        """
        data_block_iterable = PhotoDataBlockRequestIterable(name, photo_path)

        try:
            response = self.stub.UploadPhoto(data_block_iterable)
            print('Photo uploaded.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value())) #pylint: disable=no-member

    def create_and_upload_photo(self, parent, display_name, photo_path):
        """Creates and uploads a photo.

        Arguments:
            parent: The resource name of a user.
            display_name: The display name of a photo.
            photo_path: Path to a binary image file.
        
        Returns:
            photo (Photo): The photo created.
        """
        photo = self.create_photo(parent, display_name)
        self.upload_photo(photo.name, photo_path)

        print('Photo created and uploaded')
        return photo

    def list_photos(self, parent, order_by=1, page_token=None):
        """Lists photos.

        Arguments:
            parent: The resource name of a user.
            order_by: The preferred order of returned results.
            page_token: The token for next page of results.
        
        Returns:
            list (ListPhotosResponseIterable): An iteration of photos.
        """
        request = example_pb2.ListPhotosRequest(
            parent=parent,
            order_by=order_by,
            page_token=page_token
        )

        try:
            response = self.stub.ListPhotos(request)
            return ListPhotosResponseIterable(self.stub, response)
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member

    def get_photo(self, name):
        request = example_pb2.GetPhotoRequest(
            name=name
        )

        try:
            response = self.stub.GetPhoto(request)
            print('Photo fetched.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member

    def delete_photo(self, name):
        """Deletes a photo.

        Arguments:
            name: The resource name of a photo.
        
        Returns:
            None; outputs to the terminal.
        """
        request = example_pb2.DeletePhotoRequest(
            name=name
        )

        try:
            response = self.stub.DeletePhoto(request)
            print('Photo deleted.')
            return response
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member

    def stream_photos(self, names):
        """Streams photos.

        Arguments:
            names: A list of resource names of photos.
        
        Returns:
            None; outputs to the terminal.
        """
        def convert_name_to_get_photo_request(name):
            return example_pb2.GetPhotoRequest(
                name=name
            )
        
        get_photo_requests = list(map(convert_name_to_get_photo_request, names))
        get_photo_request_iterator = iter(get_photo_requests)
        try:
            response_iterator = self.stub.StreamPhotos(get_photo_request_iterator)
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member
        
        print('Receving photos:')
        for response in response_iterator:
            print(response)
