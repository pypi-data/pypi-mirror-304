# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geospatial_toolkit_grpc_service/protos/function_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9geospatial_toolkit_grpc_service/protos/function_api.proto\"E\n\x14\x43\x61lculateAMSLRequest\x12\x0b\n\x03lat\x18\x01 \x01(\x02\x12\x0b\n\x03lon\x18\x02 \x01(\x02\x12\x13\n\x0bheight_feet\x18\x03 \x01(\x02\"B\n\x15\x43\x61lculateAMSLResponse\x12\x11\n\tamsl_feet\x18\x01 \x01(\x02\x12\x16\n\x0e\x65levation_feet\x18\x02 \x01(\x02\"M\n\"ExtractShapesFromFilesAsWKTRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\x0c\"9\n#ExtractShapesFromFilesAsWKTResponse\x12\x12\n\nwkt_shapes\x18\x01 \x03(\t2\xb9\x01\n\x0b\x46unctionApi\x12>\n\rCalculateAMSL\x12\x15.CalculateAMSLRequest\x1a\x16.CalculateAMSLResponse\x12j\n\x1b\x45xtractShapesFromFilesAsWKT\x12#.ExtractShapesFromFilesAsWKTRequest\x1a$.ExtractShapesFromFilesAsWKTResponse(\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'geospatial_toolkit_grpc_service.protos.function_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CALCULATEAMSLREQUEST._serialized_start=61
  _CALCULATEAMSLREQUEST._serialized_end=130
  _CALCULATEAMSLRESPONSE._serialized_start=132
  _CALCULATEAMSLRESPONSE._serialized_end=198
  _EXTRACTSHAPESFROMFILESASWKTREQUEST._serialized_start=200
  _EXTRACTSHAPESFROMFILESASWKTREQUEST._serialized_end=277
  _EXTRACTSHAPESFROMFILESASWKTRESPONSE._serialized_start=279
  _EXTRACTSHAPESFROMFILESASWKTRESPONSE._serialized_end=336
  _FUNCTIONAPI._serialized_start=339
  _FUNCTIONAPI._serialized_end=524
# @@protoc_insertion_point(module_scope)
