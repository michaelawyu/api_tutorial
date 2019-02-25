from concurrent import futures
import time

import grpc

from codegen import example_pb2, example_pb2_grpc

class ExampleServiceServer(example_pb2_grpc.ExampleServiceServicer):
    def GetUser(self, request, context):
        name = request.name
        user = example_pb2.User(
            name=name,
            display_name='Example User',
            email='user@example.com'
        )

        return user

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleServiceServer(), server)
    server.add_insecure_port('0.0.0.0:8080')
    server.start()
    print('API server started. Listening at 0.0.0.0:8080.')
    while True:
        time.sleep(60)