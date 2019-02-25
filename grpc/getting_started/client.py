import grpc

from codegen import example_pb2, example_pb2_grpc

SERVER_ADDRESS = '0.0.0.0'
PORT = 8080

class ExampleServiceClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{PORT}')
        self.stub = example_pb2_grpc.ExampleServiceStub(self.channel)
    
    def get_user(self, name):
        request = example_pb2.GetUserRequest(
            name = name
        )

        try:
            response = self.stub.GetUser(request)
            print('User fetched.')
            print(response)
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member
