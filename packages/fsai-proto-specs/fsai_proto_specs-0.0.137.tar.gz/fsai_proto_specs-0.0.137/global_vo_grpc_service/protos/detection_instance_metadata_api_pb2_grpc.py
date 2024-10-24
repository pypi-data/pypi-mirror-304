# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from global_vo_grpc_service.protos import detection_instance_metadata_api_pb2 as global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DetectionInstanceMetadataApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListAllDetectionInstanceMetadataConfigs = channel.unary_unary(
                '/DetectionInstanceMetadataApi/ListAllDetectionInstanceMetadataConfigs',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.ListAllDetectionInstanceMetadataConfigsResponse.FromString,
                )
        self.GetMetadataByDetectionInstanceId = channel.unary_unary(
                '/DetectionInstanceMetadataApi/GetMetadataByDetectionInstanceId',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdResponse.FromString,
                )
        self.GetMetadataByDetectionInstanceIdsList = channel.unary_unary(
                '/DetectionInstanceMetadataApi/GetMetadataByDetectionInstanceIdsList',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdsListRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdsListResponse.FromString,
                )
        self.CreateDetectionInstanceMetadata = channel.unary_unary(
                '/DetectionInstanceMetadataApi/CreateDetectionInstanceMetadata',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.CreateDetectionInstanceMetadataRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.CreateDetectionInstanceMetadataResponse.FromString,
                )
        self.EditDetectionInstanceMetadata = channel.unary_unary(
                '/DetectionInstanceMetadataApi/EditDetectionInstanceMetadata',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.EditDetectionInstanceMetadataRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.EditDetectionInstanceMetadataResponse.FromString,
                )
        self.DeleteDetectionInstanceMetadata = channel.unary_unary(
                '/DetectionInstanceMetadataApi/DeleteDetectionInstanceMetadata',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.DeleteDetectionInstanceMetadataRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.DeleteDetectionInstanceMetadataResponse.FromString,
                )


class DetectionInstanceMetadataApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListAllDetectionInstanceMetadataConfigs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetadataByDetectionInstanceId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMetadataByDetectionInstanceIdsList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDetectionInstanceMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EditDetectionInstanceMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDetectionInstanceMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DetectionInstanceMetadataApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListAllDetectionInstanceMetadataConfigs': grpc.unary_unary_rpc_method_handler(
                    servicer.ListAllDetectionInstanceMetadataConfigs,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.ListAllDetectionInstanceMetadataConfigsResponse.SerializeToString,
            ),
            'GetMetadataByDetectionInstanceId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetadataByDetectionInstanceId,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdResponse.SerializeToString,
            ),
            'GetMetadataByDetectionInstanceIdsList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMetadataByDetectionInstanceIdsList,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdsListRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdsListResponse.SerializeToString,
            ),
            'CreateDetectionInstanceMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDetectionInstanceMetadata,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.CreateDetectionInstanceMetadataRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.CreateDetectionInstanceMetadataResponse.SerializeToString,
            ),
            'EditDetectionInstanceMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.EditDetectionInstanceMetadata,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.EditDetectionInstanceMetadataRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.EditDetectionInstanceMetadataResponse.SerializeToString,
            ),
            'DeleteDetectionInstanceMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDetectionInstanceMetadata,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.DeleteDetectionInstanceMetadataRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.DeleteDetectionInstanceMetadataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DetectionInstanceMetadataApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DetectionInstanceMetadataApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListAllDetectionInstanceMetadataConfigs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceMetadataApi/ListAllDetectionInstanceMetadataConfigs',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.ListAllDetectionInstanceMetadataConfigsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetadataByDetectionInstanceId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceMetadataApi/GetMetadataByDetectionInstanceId',
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMetadataByDetectionInstanceIdsList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceMetadataApi/GetMetadataByDetectionInstanceIdsList',
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdsListRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.GetMetadataByDetectionInstanceIdsListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateDetectionInstanceMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceMetadataApi/CreateDetectionInstanceMetadata',
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.CreateDetectionInstanceMetadataRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.CreateDetectionInstanceMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EditDetectionInstanceMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceMetadataApi/EditDetectionInstanceMetadata',
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.EditDetectionInstanceMetadataRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.EditDetectionInstanceMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDetectionInstanceMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceMetadataApi/DeleteDetectionInstanceMetadata',
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.DeleteDetectionInstanceMetadataRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__metadata__api__pb2.DeleteDetectionInstanceMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
