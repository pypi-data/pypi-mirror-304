# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: global_vo_grpc_service/protos/role_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from global_vo_grpc_service.protos import utils_pb2 as global__vo__grpc__service_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,global_vo_grpc_service/protos/role_api.proto\x1a)global_vo_grpc_service/protos/utils.proto\"1\n\x04Role\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07team_id\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\".\n\x17\x46indOrCreateRoleRequest\x12\x13\n\x04role\x18\x01 \x01(\x0b\x32\x05.Role\"Q\n\x18\x46indOrCreateRoleResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x13\n\x04role\x18\x02 \x01(\x0b\x32\x05.Role\"\'\n\x10ListRolesRequest\x12\x13\n\x04role\x18\x01 \x01(\x0b\x32\x05.Role\"K\n\x11ListRolesResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x14\n\x05roles\x18\x02 \x03(\x0b\x32\x05.Role2\x86\x01\n\x07RoleApi\x12G\n\x10\x46indOrCreateRole\x12\x18.FindOrCreateRoleRequest\x1a\x19.FindOrCreateRoleResponse\x12\x32\n\tListRoles\x12\x11.ListRolesRequest\x1a\x12.ListRolesResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'global_vo_grpc_service.protos.role_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ROLE._serialized_start=91
  _ROLE._serialized_end=140
  _FINDORCREATEROLEREQUEST._serialized_start=142
  _FINDORCREATEROLEREQUEST._serialized_end=188
  _FINDORCREATEROLERESPONSE._serialized_start=190
  _FINDORCREATEROLERESPONSE._serialized_end=271
  _LISTROLESREQUEST._serialized_start=273
  _LISTROLESREQUEST._serialized_end=312
  _LISTROLESRESPONSE._serialized_start=314
  _LISTROLESRESPONSE._serialized_end=389
  _ROLEAPI._serialized_start=392
  _ROLEAPI._serialized_end=526
# @@protoc_insertion_point(module_scope)
