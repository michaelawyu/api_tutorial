from concurrent import futures
import hashlib
import imghdr
import time

from google.protobuf import empty_pb2, timestamp_pb2
import grpc
import uuid

from codegen import example_pb2
from codegen import example_pb2_grpc
from models import local as model
from helpers import error_handler

API_SERVICE_NAME = '//myapiservice.com'
PAGE_SIZE = 10

class ExamplePhotoServiceServicer(example_pb2_grpc.ExamplePhotoServiceServicer):
    def CreateUser(self, request, context):
        """Creates a user.
           gRPC calls this method when clients call the CreateUser rpc (method).

        Arguments:
            request (User): The incoming request.
            context: The gRPC connection context.
        
        Returns:
            user (User): A user.
        """
        user = request

        user_id = uuid.uuid4().hex
        name = '{}/users/{}'.format(API_SERVICE_NAME, user_id)
        user.name = name
        
        # Saves the user in memory
        model.create_user(name, user)

        return user
    
    def GetUser(self, request, context):
        name = request.name

        user = model.get_user(name)
        
        if not user:
            return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified user.'
            )

        return user

    def UpdateUser(self, request, context):
        """Updates a user.
           gRPC calls this method when clients call the UpdateUser rpc (method).

        Arguments:
            request (UpdateUserRequest): The incoming request.
            context: The gRPC connection context.
        
        Returns:
            user (User): A user.
        """
        name = request.name
        updated_user = request.user
        mask = request.mask

        original_user = model.get_user(name)
        if not original_user:
            return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified user.'
            )

        mask.MergeMessage(updated_user, original_user)
        original_user.name = name
        model.update_user(name, original_user)
        
        return original_user

    def CreatePhoto(self, request, context):
        """Creates a photo.
           gRPC calls this method when clients call the CreatePhoto rpc (method).

        Arguments:
            request (CreatePhotoRequest): The incoming request.
            context: The gRPC connection context.
        
        Returns:
            photo (Photo): A user.
        """
        parent = request.parent
        photo = request.photo

        photo_id = uuid.uuid4().hex
        created_at = timestamp_pb2.Timestamp(seconds=int(time.time()))
        name = '{}/photos/{}'.format(parent, photo_id)
        photo.name = name
        photo.created_at.CopyFrom(created_at)
        try:
            # Saves the photo in memory
            model.create_photo(parent, photo)
        except ValueError:
            return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified user.'
            )

        return photo
    
    def ListPhotos(self, request, context):
        """Lists photos.
           gRPC calls this method when clients call the ListPhotos rpc (method).

        Arguments:
            request (ListPhotosRequest): The incoming request.
            context: The gRPC connection context.
        
        Returns:
            reponse (ListPhotosResponse): A ListPhotosResponse.
        """
        page_token = request.page_token

        if page_token:
            token_context = model.get_token_context(page_token)
            if not token_context:
                return error_handler.throw_exception(
                    grpc_context=context,
                    code=grpc.StatusCode.NOT_FOUND,
                    details='NOT_FOUND: Cannot find specified page token.'
                )
        else:
            token_context = {
                'parent': request.parent,
                'order_by': request.order_by,
                'offset': 0,
                'page_size': PAGE_SIZE
            }
        
        try:
            photos, if_has_more_photos = model.list_photos(**token_context)
        except ValueError:
            return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified user.'
            )

        # Prepare a new token if there are more photos
        next_page_token = None
        if if_has_more_photos:
            next_page_token = uuid.uuid4().hex
            token_context['offset'] += token_context['page_size']
            model.add_token_context(next_page_token, token_context)

        return example_pb2.ListPhotosResponse(
            photos=photos, 
            next_page_token=next_page_token
        )
    
    def GetPhoto(self, request, context):
        name = request.name
        
        photo = model.get_photo(name)
        if not photo:
             return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified photo.'
            )

        return photo

    def DeletePhoto(self, request, context):
        """Deletes a photo.
           gRPC calls this method when clients call the DeletePhoto rpc (method).

        Arguments:
            request (DeletePhotoRequest): The incoming request.
            context: The gRPC connection context.
        
        Returns:
            an Empty gRPC message.
        """
        name = request.name

        try:
            model.delete_photo(name)
        except ValueError:
            return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified photo.'
            )
        
        return empty_pb2.Empty()
    
    def UploadPhoto(self, request_iterator, context):
        """Uploads a photo.
           gRPC calls this method when clients call the UploadPhoto rpc (method).

        Arguments:
            request_iterator (iterator): An iterator of incoming requests.
            context: The gRPC connection context.
        
        Returns:
            An Empty Protocol Buffers message.
        """
        data_blocks = []
        data_hash = None
        name = None
        for request in request_iterator:
            m = hashlib.new('md5', request.data_block).hexdigest()
            if m != request.data_block_hash:
                return error_handler.throw_exception(
                    grpc_context=context,
                    code=grpc.StatusCode.DATA_LOSS,
                    details='DATA_LOSS: Datablock is corrupted.'
                )
            
            data_hash = request.data_hash
            name = request.name

            data_blocks.append(request.data_block)
            if len(data_blocks) > 100:
                return error_handler.throw_exception(
                    grpc_context=context,
                    code=grpc.StatusCode.FAILED_PRECONDITION,
                    details='FAILED_PRECONDITION: Image is oversized.'
                )
        
        data = b''.join(data_blocks)
        m = hashlib.new('md5', data).hexdigest()
        if m != data_hash:
            return error_handler.throw_exception(
                    grpc_context=context,
                    code=grpc.StatusCode.DATA_LOSS,
                    details='DATA_LOSS: Data is corrupted.'
                )

        photo_format = imghdr.what('', data)
        filename = name.replace('/', '')
        if photo_format:
            with open('photos/{}.{}'.format(filename, photo_format), 'wb') as f:
                f.write(data)
            return empty_pb2.Empty()
        else:
            return error_handler.throw_exception(
                    grpc_context=context,
                    code=grpc.StatusCode.FAILED_PRECONDITION,
                    details='FAILED_PRECONDITION: File type is not supported.'
                )

    def DownloadPhoto(self, request, context):
        pass

    def StreamPhotos(self, request_iterator, context):
        """Streams photos.
           gRPC calls this method when clients call the StreamPhotos rpc (method).

        Arguments:
            request_iterator (iterator): An iterator of incoming requests.
            context: The gRPC connection context.
        
        Returns:
            A generator.
        """
        for request in request_iterator:
            yield self.GetPhoto(request, context)

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    example_pb2_grpc.add_ExamplePhotoServiceServicer_to_server(ExamplePhotoServiceServicer(), server)
    server.add_insecure_port('0.0.0.0:8080')
    server.start()
    print('API server started. Listening at 0.0.0.0:8080.')
    print('Connection is insecure. No authentication enabled.')
    while True:
        time.sleep(60)
