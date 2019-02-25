import grpc

from codegen import example_pb2, example_pb2_grpc

SERVER_ADDRESS = '0.0.0.0'
PORT = 8080

class ExampleServiceClient(object):
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
        self.stub = example_pb2_grpc.ExampleServiceStub(self.channel)
    
    def get_user(self, name):
        """Gets a user.
        Arguments:
            name: The resource name of a user.
        
        Returns:
            None; outputs to the terminal.
        """
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
