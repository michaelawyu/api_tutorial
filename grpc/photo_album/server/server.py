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

class ExamplePhotoServiceServer(example_pb2_grpc.ExamplePhotoServiceServicer):
    def CreateUser(self, request, context):
        user = request.user

        user_id = uuid.uuid4().hex
        name = '{}/users/{}'.format(API_SERVICE_NAME, user_id)
        user.name = name
        
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
        updated_user.name = name
        model.update_user(name, updated_user)
        
        return updated_user

    def CreatePhoto(self, request, context):
        parent = request.parent
        photo = request.photo

        photo_id = uuid.uuid4().hex
        created_at = timestamp_pb2.Timestamp(seconds=int(time.time()))
        name = '//{}/users/{}/photos/{}'.format(API_SERVICE_NAME, parent,
                                                photo_id)
        photo.name = name
        photo.created_at.CopyFrom(created_at)
        try:
            model.create_photo(parent, photo)
        except ValueError:
            return error_handler.throw_exception(
                grpc_context=context,
                code=grpc.StatusCode.NOT_FOUND,
                details='NOT_FOUND: Cannot find specified user.'
            )

        return photo
    
    def ListPhotos(self, request, context):
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
        for request in request_iterator:
            yield self.GetPhoto(request, context)

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    example_pb2_grpc.add_ExamplePhotoServiceServicer_to_server(ExamplePhotoServiceServer(), server)
    server.add_insecure_port('0.0.0.0:8080')
    server.start()
    print('API server started. Listening at 0.0.0.0:8080.')
    print('Connection is insecure. No authentication enabled.')
    while True:
        time.sleep(60)
