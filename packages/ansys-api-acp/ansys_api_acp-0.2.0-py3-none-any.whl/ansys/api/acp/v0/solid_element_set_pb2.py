# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/acp/v0/solid_element_set.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ansys.api.acp.v0 import base_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_base__pb2
from ansys.api.acp.v0 import enum_types_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_enum__types__pb2
from ansys.api.acp.v0 import array_types_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_array__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(ansys/api/acp/v0/solid_element_set.proto\x12\"ansys.api.acp.v0.solid_element_set\x1a\x1b\x61nsys/api/acp/v0/base.proto\x1a!ansys/api/acp/v0/enum_types.proto\x1a\"ansys/api/acp/v0/array_types.proto\"\x95\x01\n\nProperties\x12\x37\n\x06status\x18\x01 \x01(\x0e\x32\'.ansys.api.acp.v0.enum_types.StatusType\x12\x0e\n\x06locked\x18\x02 \x01(\x08\x12>\n\x0e\x65lement_labels\x18\x03 \x01(\x0b\x32&.ansys.api.acp.v0.array_types.IntArray\"\x80\x01\n\nObjectInfo\x12.\n\x04info\x18\x01 \x01(\x0b\x32 .ansys.api.acp.v0.base.BasicInfo\x12\x42\n\nproperties\x18\x02 \x01(\x0b\x32..ansys.api.acp.v0.solid_element_set.Properties\"L\n\tListReply\x12?\n\x07objects\x18\x01 \x03(\x0b\x32..ansys.api.acp.v0.solid_element_set.ObjectInfo2\xc4\x01\n\rObjectService\x12Y\n\x04List\x12\".ansys.api.acp.v0.base.ListRequest\x1a-.ansys.api.acp.v0.solid_element_set.ListReply\x12X\n\x03Get\x12!.ansys.api.acp.v0.base.GetRequest\x1a..ansys.api.acp.v0.solid_element_set.ObjectInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.acp.v0.solid_element_set_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PROPERTIES._serialized_start=181
  _PROPERTIES._serialized_end=330
  _OBJECTINFO._serialized_start=333
  _OBJECTINFO._serialized_end=461
  _LISTREPLY._serialized_start=463
  _LISTREPLY._serialized_end=539
  _OBJECTSERVICE._serialized_start=542
  _OBJECTSERVICE._serialized_end=738
# @@protoc_insertion_point(module_scope)
