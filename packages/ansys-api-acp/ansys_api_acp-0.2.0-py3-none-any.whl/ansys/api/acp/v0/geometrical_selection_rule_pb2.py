# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/acp/v0/geometrical_selection_rule.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ansys.api.acp.v0 import base_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_base__pb2
from ansys.api.acp.v0 import enum_types_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_enum__types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1ansys/api/acp/v0/geometrical_selection_rule.proto\x12+ansys.api.acp.v0.geometrical_selection_rule\x1a\x1b\x61nsys/api/acp/v0/base.proto\x1a!ansys/api/acp/v0/enum_types.proto\"\xbf\x03\n\nProperties\x12\x37\n\x06status\x18\x01 \x01(\x0e\x32\'.ansys.api.acp.v0.enum_types.StatusType\x12_\n\x15geometrical_rule_type\x18\x02 \x01(\x0e\x32@.ansys.api.acp.v0.geometrical_selection_rule.GeometricalRuleType\x12\x35\n\x08geometry\x18\x03 \x01(\x0b\x32#.ansys.api.acp.v0.base.ResourcePath\x12\x39\n\x0c\x65lement_sets\x18\x04 \x03(\x0b\x32#.ansys.api.acp.v0.base.ResourcePath\x12\x19\n\x11include_rule_type\x18\x05 \x01(\x08\x12\x1e\n\x16use_default_tolerances\x18\x06 \x01(\x08\x12\"\n\x1ain_plane_capture_tolerance\x18\x07 \x01(\x01\x12\"\n\x1anegative_capture_tolerance\x18\x08 \x01(\x01\x12\"\n\x1apositive_capture_tolerance\x18\t \x01(\x01\"\x89\x01\n\nObjectInfo\x12.\n\x04info\x18\x01 \x01(\x0b\x32 .ansys.api.acp.v0.base.BasicInfo\x12K\n\nproperties\x18\x02 \x01(\x0b\x32\x37.ansys.api.acp.v0.geometrical_selection_rule.Properties\"U\n\tListReply\x12H\n\x07objects\x18\x01 \x03(\x0b\x32\x37.ansys.api.acp.v0.geometrical_selection_rule.ObjectInfo\"\xaa\x01\n\rCreateRequest\x12>\n\x0f\x63ollection_path\x18\x01 \x01(\x0b\x32%.ansys.api.acp.v0.base.CollectionPath\x12\x0c\n\x04name\x18\x02 \x01(\t\x12K\n\nproperties\x18\x03 \x01(\x0b\x32\x37.ansys.api.acp.v0.geometrical_selection_rule.Properties*5\n\x13GeometricalRuleType\x12\x0c\n\x08GEOMETRY\x10\x00\x12\x10\n\x0c\x45LEMENT_SETS\x10\x01\x32\x9c\x04\n\rObjectService\x12\x62\n\x04List\x12\".ansys.api.acp.v0.base.ListRequest\x1a\x36.ansys.api.acp.v0.geometrical_selection_rule.ListReply\x12\x61\n\x03Get\x12!.ansys.api.acp.v0.base.GetRequest\x1a\x37.ansys.api.acp.v0.geometrical_selection_rule.ObjectInfo\x12w\n\x03Put\x12\x37.ansys.api.acp.v0.geometrical_selection_rule.ObjectInfo\x1a\x37.ansys.api.acp.v0.geometrical_selection_rule.ObjectInfo\x12L\n\x06\x44\x65lete\x12$.ansys.api.acp.v0.base.DeleteRequest\x1a\x1c.ansys.api.acp.v0.base.Empty\x12}\n\x06\x43reate\x12:.ansys.api.acp.v0.geometrical_selection_rule.CreateRequest\x1a\x37.ansys.api.acp.v0.geometrical_selection_rule.ObjectInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.acp.v0.geometrical_selection_rule_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GEOMETRICALRULETYPE._serialized_start=1012
  _GEOMETRICALRULETYPE._serialized_end=1065
  _PROPERTIES._serialized_start=163
  _PROPERTIES._serialized_end=610
  _OBJECTINFO._serialized_start=613
  _OBJECTINFO._serialized_end=750
  _LISTREPLY._serialized_start=752
  _LISTREPLY._serialized_end=837
  _CREATEREQUEST._serialized_start=840
  _CREATEREQUEST._serialized_end=1010
  _OBJECTSERVICE._serialized_start=1068
  _OBJECTSERVICE._serialized_end=1608
# @@protoc_insertion_point(module_scope)
