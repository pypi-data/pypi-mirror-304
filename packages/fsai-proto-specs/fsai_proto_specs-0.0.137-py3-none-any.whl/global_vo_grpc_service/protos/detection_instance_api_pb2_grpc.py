# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from global_vo_grpc_service.protos import detection_instance_api_pb2 as global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2


class DetectionInstanceApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateDetectionInstanceViaMachine = channel.unary_unary(
                '/DetectionInstanceApi/CreateDetectionInstanceViaMachine',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaMachineRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaMachineResponse.FromString,
                )
        self.CreateDetectionInstanceViaHuman = channel.unary_unary(
                '/DetectionInstanceApi/CreateDetectionInstanceViaHuman',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaHumanRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaHumanResponse.FromString,
                )
        self.DeleteDetectionInstanceById = channel.unary_unary(
                '/DetectionInstanceApi/DeleteDetectionInstanceById',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.DeleteDetectionInstanceByIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.DeleteDetectionInstanceByIdResponse.FromString,
                )
        self.GetDetectionInstanceBboxById = channel.unary_unary(
                '/DetectionInstanceApi/GetDetectionInstanceBboxById',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceBboxByIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceBboxByIdResponse.FromString,
                )
        self.GetDetectionInstanceStateById = channel.unary_unary(
                '/DetectionInstanceApi/GetDetectionInstanceStateById',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceStateByIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceStateByIdResponse.FromString,
                )
        self.GetDetectionInstanceByIds = channel.unary_unary(
                '/DetectionInstanceApi/GetDetectionInstanceByIds',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceByIdsRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceByIdsResponse.FromString,
                )
        self.GetDetectionInstancesByImageId = channel.unary_unary(
                '/DetectionInstanceApi/GetDetectionInstancesByImageId',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByImageIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByImageIdResponse.FromString,
                )
        self.GetDetectionInstancesByH3Cell = channel.unary_unary(
                '/DetectionInstanceApi/GetDetectionInstancesByH3Cell',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByH3CellRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByH3CellResponse.FromString,
                )
        self.TransitionDetectionInstanceState = channel.unary_unary(
                '/DetectionInstanceApi/TransitionDetectionInstanceState',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.TransitionDetectionInstanceStateRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.TransitionDetectionInstanceStateResponse.FromString,
                )
        self.UpdateDetectionInstanceCategoryId = channel.unary_unary(
                '/DetectionInstanceApi/UpdateDetectionInstanceCategoryId',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceCategoryIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceCategoryIdResponse.FromString,
                )
        self.UpdateDetectionInstanceGeoBboxViaHuman = channel.unary_unary(
                '/DetectionInstanceApi/UpdateDetectionInstanceGeoBboxViaHuman',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoBboxViaHumanRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoBboxViaHumanResponse.FromString,
                )
        self.UpdateDetectionInstanceGeoPointsViaHuman = channel.unary_unary(
                '/DetectionInstanceApi/UpdateDetectionInstanceGeoPointsViaHuman',
                request_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoPointsViaHumanRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoPointsViaHumanResponse.FromString,
                )


class DetectionInstanceApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateDetectionInstanceViaMachine(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDetectionInstanceViaHuman(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDetectionInstanceById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDetectionInstanceBboxById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDetectionInstanceStateById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDetectionInstanceByIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDetectionInstancesByImageId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDetectionInstancesByH3Cell(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TransitionDetectionInstanceState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDetectionInstanceCategoryId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDetectionInstanceGeoBboxViaHuman(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDetectionInstanceGeoPointsViaHuman(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DetectionInstanceApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateDetectionInstanceViaMachine': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDetectionInstanceViaMachine,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaMachineRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaMachineResponse.SerializeToString,
            ),
            'CreateDetectionInstanceViaHuman': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDetectionInstanceViaHuman,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaHumanRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaHumanResponse.SerializeToString,
            ),
            'DeleteDetectionInstanceById': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDetectionInstanceById,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.DeleteDetectionInstanceByIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.DeleteDetectionInstanceByIdResponse.SerializeToString,
            ),
            'GetDetectionInstanceBboxById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDetectionInstanceBboxById,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceBboxByIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceBboxByIdResponse.SerializeToString,
            ),
            'GetDetectionInstanceStateById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDetectionInstanceStateById,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceStateByIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceStateByIdResponse.SerializeToString,
            ),
            'GetDetectionInstanceByIds': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDetectionInstanceByIds,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceByIdsRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceByIdsResponse.SerializeToString,
            ),
            'GetDetectionInstancesByImageId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDetectionInstancesByImageId,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByImageIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByImageIdResponse.SerializeToString,
            ),
            'GetDetectionInstancesByH3Cell': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDetectionInstancesByH3Cell,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByH3CellRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByH3CellResponse.SerializeToString,
            ),
            'TransitionDetectionInstanceState': grpc.unary_unary_rpc_method_handler(
                    servicer.TransitionDetectionInstanceState,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.TransitionDetectionInstanceStateRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.TransitionDetectionInstanceStateResponse.SerializeToString,
            ),
            'UpdateDetectionInstanceCategoryId': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDetectionInstanceCategoryId,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceCategoryIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceCategoryIdResponse.SerializeToString,
            ),
            'UpdateDetectionInstanceGeoBboxViaHuman': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDetectionInstanceGeoBboxViaHuman,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoBboxViaHumanRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoBboxViaHumanResponse.SerializeToString,
            ),
            'UpdateDetectionInstanceGeoPointsViaHuman': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDetectionInstanceGeoPointsViaHuman,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoPointsViaHumanRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoPointsViaHumanResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DetectionInstanceApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DetectionInstanceApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateDetectionInstanceViaMachine(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/CreateDetectionInstanceViaMachine',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaMachineRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaMachineResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateDetectionInstanceViaHuman(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/CreateDetectionInstanceViaHuman',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaHumanRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.CreateDetectionInstanceViaHumanResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDetectionInstanceById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/DeleteDetectionInstanceById',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.DeleteDetectionInstanceByIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.DeleteDetectionInstanceByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDetectionInstanceBboxById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/GetDetectionInstanceBboxById',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceBboxByIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceBboxByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDetectionInstanceStateById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/GetDetectionInstanceStateById',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceStateByIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceStateByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDetectionInstanceByIds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/GetDetectionInstanceByIds',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceByIdsRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstanceByIdsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDetectionInstancesByImageId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/GetDetectionInstancesByImageId',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByImageIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByImageIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDetectionInstancesByH3Cell(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/GetDetectionInstancesByH3Cell',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByH3CellRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.GetDetectionInstancesByH3CellResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TransitionDetectionInstanceState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/TransitionDetectionInstanceState',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.TransitionDetectionInstanceStateRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.TransitionDetectionInstanceStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDetectionInstanceCategoryId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/UpdateDetectionInstanceCategoryId',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceCategoryIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceCategoryIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDetectionInstanceGeoBboxViaHuman(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/UpdateDetectionInstanceGeoBboxViaHuman',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoBboxViaHumanRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoBboxViaHumanResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDetectionInstanceGeoPointsViaHuman(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionInstanceApi/UpdateDetectionInstanceGeoPointsViaHuman',
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoPointsViaHumanRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_detection__instance__api__pb2.UpdateDetectionInstanceGeoPointsViaHumanResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
