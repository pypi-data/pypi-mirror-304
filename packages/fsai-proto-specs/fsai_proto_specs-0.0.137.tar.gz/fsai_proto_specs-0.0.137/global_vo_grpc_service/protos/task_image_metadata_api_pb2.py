# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: global_vo_grpc_service/protos/task_image_metadata_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from global_vo_grpc_service.protos import utils_pb2 as global__vo__grpc__service_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;global_vo_grpc_service/protos/task_image_metadata_api.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a)global_vo_grpc_service/protos/utils.proto\"F\n\x13PrimaryIssueConfigs\x12\x0c\n\x04\x65num\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"Y\n\"ListAllPrimaryIssueConfigsResponse\x12\x33\n\x15primary_issue_configs\x18\x01 \x03(\x0b\x32\x14.PrimaryIssueConfigs\"\xe3\x01\n\x11TaskImageMetadata\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x15\n\rtask_image_id\x18\x02 \x01(\x05\x12\x0b\n\x03key\x18\x03 \x01(\t\x12\x16\n\x0evalue_json_str\x18\x04 \x01(\t\x12\x12\n\ncreated_by\x18\x05 \x01(\x05\x12\x12\n\nupdated_by\x18\x06 \x01(\x05\x12.\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"A\n(GetTaskImageMetadataByTaskImageIdRequest\x12\x15\n\rtask_image_id\x18\x01 \x01(\x05\"\\\n)GetTaskImageMetadataByTaskImageIdResponse\x12/\n\x13task_image_metadata\x18\x01 \x03(\x0b\x32\x12.TaskImageMetadata\"\\\n\x1e\x43reateTaskImageMetadataRequest\x12\x15\n\rtask_image_id\x18\x01 \x01(\x05\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x16\n\x0evalue_json_str\x18\x03 \x01(\t\"O\n\x1f\x43reateTaskImageMetadataResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\n\n\x02id\x18\x02 \x01(\x05\"\\\n\x1eUpdateTaskImageMetadataRequest\x12\x15\n\rtask_image_id\x18\x01 \x01(\x05\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x16\n\x0evalue_json_str\x18\x03 \x01(\t\"O\n\x1fUpdateTaskImageMetadataResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\n\n\x02id\x18\x02 \x01(\x05\",\n\x1e\x44\x65leteTaskImageMetadataRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"C\n\x1f\x44\x65leteTaskImageMetadataResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType2\x87\x04\n\x14TaskImageMetadataApi\x12Y\n\x1aListAllPrimaryIssueConfigs\x12\x16.google.protobuf.Empty\x1a#.ListAllPrimaryIssueConfigsResponse\x12z\n!GetTaskImageMetadataByTaskImageId\x12).GetTaskImageMetadataByTaskImageIdRequest\x1a*.GetTaskImageMetadataByTaskImageIdResponse\x12\\\n\x17\x43reateTaskImageMetadata\x12\x1f.CreateTaskImageMetadataRequest\x1a .CreateTaskImageMetadataResponse\x12\\\n\x17UpdateTaskImageMetadata\x12\x1f.UpdateTaskImageMetadataRequest\x1a .UpdateTaskImageMetadataResponse\x12\\\n\x17\x44\x65leteTaskImageMetadata\x12\x1f.DeleteTaskImageMetadataRequest\x1a .DeleteTaskImageMetadataResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'global_vo_grpc_service.protos.task_image_metadata_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PRIMARYISSUECONFIGS._serialized_start=168
  _PRIMARYISSUECONFIGS._serialized_end=238
  _LISTALLPRIMARYISSUECONFIGSRESPONSE._serialized_start=240
  _LISTALLPRIMARYISSUECONFIGSRESPONSE._serialized_end=329
  _TASKIMAGEMETADATA._serialized_start=332
  _TASKIMAGEMETADATA._serialized_end=559
  _GETTASKIMAGEMETADATABYTASKIMAGEIDREQUEST._serialized_start=561
  _GETTASKIMAGEMETADATABYTASKIMAGEIDREQUEST._serialized_end=626
  _GETTASKIMAGEMETADATABYTASKIMAGEIDRESPONSE._serialized_start=628
  _GETTASKIMAGEMETADATABYTASKIMAGEIDRESPONSE._serialized_end=720
  _CREATETASKIMAGEMETADATAREQUEST._serialized_start=722
  _CREATETASKIMAGEMETADATAREQUEST._serialized_end=814
  _CREATETASKIMAGEMETADATARESPONSE._serialized_start=816
  _CREATETASKIMAGEMETADATARESPONSE._serialized_end=895
  _UPDATETASKIMAGEMETADATAREQUEST._serialized_start=897
  _UPDATETASKIMAGEMETADATAREQUEST._serialized_end=989
  _UPDATETASKIMAGEMETADATARESPONSE._serialized_start=991
  _UPDATETASKIMAGEMETADATARESPONSE._serialized_end=1070
  _DELETETASKIMAGEMETADATAREQUEST._serialized_start=1072
  _DELETETASKIMAGEMETADATAREQUEST._serialized_end=1116
  _DELETETASKIMAGEMETADATARESPONSE._serialized_start=1118
  _DELETETASKIMAGEMETADATARESPONSE._serialized_end=1185
  _TASKIMAGEMETADATAAPI._serialized_start=1188
  _TASKIMAGEMETADATAAPI._serialized_end=1707
# @@protoc_insertion_point(module_scope)
