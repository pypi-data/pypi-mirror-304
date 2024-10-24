# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/acp/v0/spherical_selection_rule.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/ansys/api/acp/v0/spherical_selection_rule.proto\x12)ansys.api.acp.v0.spherical_selection_rule\x1a\x1b\x61nsys/api/acp/v0/base.proto\x1a!ansys/api/acp/v0/enum_types.proto\x1a\"ansys/api/acp/v0/array_types.proto\"\xa3\x02\n\nProperties\x12\x37\n\x06status\x18\x01 \x01(\x0e\x32\'.ansys.api.acp.v0.enum_types.StatusType\x12$\n\x1cuse_global_coordinate_system\x18\x02 \x01(\x08\x12\x34\n\x07rosette\x18\x03 \x01(\x0b\x32#.ansys.api.acp.v0.base.ResourcePath\x12\x39\n\x06origin\x18\x04 \x01(\x0b\x32).ansys.api.acp.v0.array_types.DoubleArray\x12\x0e\n\x06radius\x18\x05 \x01(\x01\x12\x1a\n\x12relative_rule_type\x18\x06 \x01(\x08\x12\x19\n\x11include_rule_type\x18\x07 \x01(\x08\"\x87\x01\n\nObjectInfo\x12.\n\x04info\x18\x01 \x01(\x0b\x32 .ansys.api.acp.v0.base.BasicInfo\x12I\n\nproperties\x18\x02 \x01(\x0b\x32\x35.ansys.api.acp.v0.spherical_selection_rule.Properties\"S\n\tListReply\x12\x46\n\x07objects\x18\x01 \x03(\x0b\x32\x35.ansys.api.acp.v0.spherical_selection_rule.ObjectInfo\"\xa8\x01\n\rCreateRequest\x12>\n\x0f\x63ollection_path\x18\x01 \x01(\x0b\x32%.ansys.api.acp.v0.base.CollectionPath\x12\x0c\n\x04name\x18\x02 \x01(\t\x12I\n\nproperties\x18\x03 \x01(\x0b\x32\x35.ansys.api.acp.v0.spherical_selection_rule.Properties2\x90\x04\n\rObjectService\x12`\n\x04List\x12\".ansys.api.acp.v0.base.ListRequest\x1a\x34.ansys.api.acp.v0.spherical_selection_rule.ListReply\x12_\n\x03Get\x12!.ansys.api.acp.v0.base.GetRequest\x1a\x35.ansys.api.acp.v0.spherical_selection_rule.ObjectInfo\x12s\n\x03Put\x12\x35.ansys.api.acp.v0.spherical_selection_rule.ObjectInfo\x1a\x35.ansys.api.acp.v0.spherical_selection_rule.ObjectInfo\x12L\n\x06\x44\x65lete\x12$.ansys.api.acp.v0.base.DeleteRequest\x1a\x1c.ansys.api.acp.v0.base.Empty\x12y\n\x06\x43reate\x12\x38.ansys.api.acp.v0.spherical_selection_rule.CreateRequest\x1a\x35.ansys.api.acp.v0.spherical_selection_rule.ObjectInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.acp.v0.spherical_selection_rule_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PROPERTIES._serialized_start=195
  _PROPERTIES._serialized_end=486
  _OBJECTINFO._serialized_start=489
  _OBJECTINFO._serialized_end=624
  _LISTREPLY._serialized_start=626
  _LISTREPLY._serialized_end=709
  _CREATEREQUEST._serialized_start=712
  _CREATEREQUEST._serialized_end=880
  _OBJECTSERVICE._serialized_start=883
  _OBJECTSERVICE._serialized_end=1411
# @@protoc_insertion_point(module_scope)
