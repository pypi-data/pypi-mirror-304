# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from geospatial_toolkit_grpc_service.protos import mgrs_api_pb2 as geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2


class MGRSApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CalculateLatLonFromMGRS = channel.unary_unary(
                '/MGRSApi/CalculateLatLonFromMGRS',
                request_serializer=geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2.CalculateLatLonFromMGRSRequest.SerializeToString,
                response_deserializer=geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2.CalculateLatLonFromMGRSResponse.FromString,
                )


class MGRSApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CalculateLatLonFromMGRS(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MGRSApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CalculateLatLonFromMGRS': grpc.unary_unary_rpc_method_handler(
                    servicer.CalculateLatLonFromMGRS,
                    request_deserializer=geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2.CalculateLatLonFromMGRSRequest.FromString,
                    response_serializer=geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2.CalculateLatLonFromMGRSResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'MGRSApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MGRSApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CalculateLatLonFromMGRS(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/MGRSApi/CalculateLatLonFromMGRS',
            geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2.CalculateLatLonFromMGRSRequest.SerializeToString,
            geospatial__toolkit__grpc__service_dot_protos_dot_mgrs__api__pb2.CalculateLatLonFromMGRSResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
