# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from data_grpc_service.protos import image_data_api_pb2 as data__grpc__service_dot_protos_dot_image__data__api__pb2


class ImageDataApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetImageDataById = channel.unary_stream(
                '/ImageDataApi/GetImageDataById',
                request_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdRequest.SerializeToString,
                response_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdResponse.FromString,
                )
        self.FindImageKeyById = channel.unary_unary(
                '/ImageDataApi/FindImageKeyById',
                request_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.FindImageKeyByIdRequest.SerializeToString,
                response_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.FindImageKeyByIdResponse.FromString,
                )
        self.UpdateImageStoreById = channel.unary_unary(
                '/ImageDataApi/UpdateImageStoreById',
                request_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.UpdateImageStoreByIdRequest.SerializeToString,
                response_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.UpdateImageStoreByIdResponse.FromString,
                )
        self.DeleteImageOnDisk = channel.unary_unary(
                '/ImageDataApi/DeleteImageOnDisk',
                request_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.DeleteImageOnDiskRequest.SerializeToString,
                response_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.DeleteImageOnDiskResponse.FromString,
                )


class ImageDataApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetImageDataById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindImageKeyById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateImageStoreById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteImageOnDisk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageDataApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetImageDataById': grpc.unary_stream_rpc_method_handler(
                    servicer.GetImageDataById,
                    request_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdRequest.FromString,
                    response_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdResponse.SerializeToString,
            ),
            'FindImageKeyById': grpc.unary_unary_rpc_method_handler(
                    servicer.FindImageKeyById,
                    request_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.FindImageKeyByIdRequest.FromString,
                    response_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.FindImageKeyByIdResponse.SerializeToString,
            ),
            'UpdateImageStoreById': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateImageStoreById,
                    request_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.UpdateImageStoreByIdRequest.FromString,
                    response_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.UpdateImageStoreByIdResponse.SerializeToString,
            ),
            'DeleteImageOnDisk': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteImageOnDisk,
                    request_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.DeleteImageOnDiskRequest.FromString,
                    response_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.DeleteImageOnDiskResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ImageDataApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageDataApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetImageDataById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ImageDataApi/GetImageDataById',
            data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdRequest.SerializeToString,
            data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FindImageKeyById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageDataApi/FindImageKeyById',
            data__grpc__service_dot_protos_dot_image__data__api__pb2.FindImageKeyByIdRequest.SerializeToString,
            data__grpc__service_dot_protos_dot_image__data__api__pb2.FindImageKeyByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateImageStoreById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageDataApi/UpdateImageStoreById',
            data__grpc__service_dot_protos_dot_image__data__api__pb2.UpdateImageStoreByIdRequest.SerializeToString,
            data__grpc__service_dot_protos_dot_image__data__api__pb2.UpdateImageStoreByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteImageOnDisk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ImageDataApi/DeleteImageOnDisk',
            data__grpc__service_dot_protos_dot_image__data__api__pb2.DeleteImageOnDiskRequest.SerializeToString,
            data__grpc__service_dot_protos_dot_image__data__api__pb2.DeleteImageOnDiskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
