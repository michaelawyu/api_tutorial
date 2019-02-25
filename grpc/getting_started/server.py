from concurrent import futures
import time

import grpc

from codegen import example_pb2, example_pb2_grpc

# Inherit from example_pb2_grpc.ExampleServiceServicer
# ExampleServiceServicer is the server-side artifact.
class ExampleServiceServicer(example_pb2_grpc.ExampleServiceServicer): 
    def GetUser(self, request, context):
        """Gets a user.
           gRPC calls this method when clients call the GetUser rpc (method).

        Arguments:
            request (GetUserRequest): The incoming request.
            context: The gRPC connection context.
        
        Returns:
            user (User): A user.
        """
        name = request.name
        user = example_pb2.User(
            name=name,
            display_name='Example User',
            email='user@example.com'
        )

        return user

if __name__ == '__main__':
    # Run a gRPC server with one thread.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    # Adds the servicer class to the server.
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServiceServicer(), server)
    server.add_insecure_port('0.0.0.0:8080')
    server.start()
    print('API server started. Listening at 0.0.0.0:8080.')
    while True:
        time.sleep(60)