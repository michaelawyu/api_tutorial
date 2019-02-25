from google.protobuf import empty_pb2

def throw_exception(grpc_context, code, details):
    grpc_context.set_details(details)
    grpc_context.set_code(code)
    return empty_pb2.Empty()
