# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ansys/api/acp/v0/fabric.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ansys.api.acp.v0 import base_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_base__pb2
from ansys.api.acp.v0 import enum_types_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_enum__types__pb2
from ansys.api.acp.v0 import ply_material_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_ply__material__pb2
from ansys.api.acp.v0 import cut_off_material_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_cut__off__material__pb2
from ansys.api.acp.v0 import drop_off_material_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_drop__off__material__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x61nsys/api/acp/v0/fabric.proto\x12\x17\x61nsys.api.acp.v0.fabric\x1a\x1b\x61nsys/api/acp/v0/base.proto\x1a!ansys/api/acp/v0/enum_types.proto\x1a#ansys/api/acp/v0/ply_material.proto\x1a\'ansys/api/acp/v0/cut_off_material.proto\x1a(ansys/api/acp/v0/drop_off_material.proto\"\x88\x05\n\nProperties\x12\x37\n\x06status\x18\x01 \x01(\x0e\x32\'.ansys.api.acp.v0.enum_types.StatusType\x12\x35\n\x08material\x18\t \x01(\x0b\x32#.ansys.api.acp.v0.base.ResourcePath\x12\x11\n\tthickness\x18\x02 \x01(\x01\x12\x12\n\narea_price\x18\x03 \x01(\x01\x12!\n\x19ignore_for_postprocessing\x18\x04 \x01(\x08\x12\\\n\x1a\x64rop_off_material_handling\x18\x05 \x01(\x0e\x32\x38.ansys.api.acp.v0.drop_off_material.MaterialHandlingType\x12>\n\x11\x64rop_off_material\x18\x0b \x01(\x0b\x32#.ansys.api.acp.v0.base.ResourcePath\x12Z\n\x19\x63ut_off_material_handling\x18\x06 \x01(\x0e\x32\x37.ansys.api.acp.v0.cut_off_material.MaterialHandlingType\x12=\n\x10\x63ut_off_material\x18\x0c \x01(\x0b\x32#.ansys.api.acp.v0.base.ResourcePath\x12R\n\x16\x64raping_material_model\x18\x07 \x01(\x0e\x32\x32.ansys.api.acp.v0.ply_material.DrapingMaterialType\x12\x1e\n\x16\x64raping_ud_coefficient\x18\x08 \x01(\x01\x12\x13\n\x0b\x61rea_weight\x18\n \x01(\x01\"u\n\nObjectInfo\x12.\n\x04info\x18\x01 \x01(\x0b\x32 .ansys.api.acp.v0.base.BasicInfo\x12\x37\n\nproperties\x18\x02 \x01(\x0b\x32#.ansys.api.acp.v0.fabric.Properties\"A\n\tListReply\x12\x34\n\x07objects\x18\x01 \x03(\x0b\x32#.ansys.api.acp.v0.fabric.ObjectInfo\"\x96\x01\n\rCreateRequest\x12>\n\x0f\x63ollection_path\x18\x01 \x01(\x0b\x32%.ansys.api.acp.v0.base.CollectionPath\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x37\n\nproperties\x18\x03 \x01(\x0b\x32#.ansys.api.acp.v0.fabric.Properties2\xa4\x03\n\rObjectService\x12N\n\x04List\x12\".ansys.api.acp.v0.base.ListRequest\x1a\".ansys.api.acp.v0.fabric.ListReply\x12M\n\x03Get\x12!.ansys.api.acp.v0.base.GetRequest\x1a#.ansys.api.acp.v0.fabric.ObjectInfo\x12O\n\x03Put\x12#.ansys.api.acp.v0.fabric.ObjectInfo\x1a#.ansys.api.acp.v0.fabric.ObjectInfo\x12L\n\x06\x44\x65lete\x12$.ansys.api.acp.v0.base.DeleteRequest\x1a\x1c.ansys.api.acp.v0.base.Empty\x12U\n\x06\x43reate\x12&.ansys.api.acp.v0.fabric.CreateRequest\x1a#.ansys.api.acp.v0.fabric.ObjectInfob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ansys.api.acp.v0.fabric_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _PROPERTIES._serialized_start=243
  _PROPERTIES._serialized_end=891
  _OBJECTINFO._serialized_start=893
  _OBJECTINFO._serialized_end=1010
  _LISTREPLY._serialized_start=1012
  _LISTREPLY._serialized_end=1077
  _CREATEREQUEST._serialized_start=1080
  _CREATEREQUEST._serialized_end=1230
  _OBJECTSERVICE._serialized_start=1233
  _OBJECTSERVICE._serialized_end=1653
# @@protoc_insertion_point(module_scope)
