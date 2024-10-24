"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import ansys.api.acp.v0.base_pb2
import ansys.api.acp.v0.cut_off_material_pb2
import ansys.api.acp.v0.drop_off_material_pb2
import ansys.api.acp.v0.enum_types_pb2
import ansys.api.acp.v0.ply_material_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class FabricWithAngle(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FABRIC_FIELD_NUMBER: builtins.int
    ANGLE_FIELD_NUMBER: builtins.int
    @property
    def fabric(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    angle: builtins.float = ...
    def __init__(self,
        *,
        fabric : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        angle : builtins.float = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["fabric",b"fabric"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["angle",b"angle","fabric",b"fabric"]) -> None: ...
global___FabricWithAngle = FabricWithAngle

class Properties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    STATUS_FIELD_NUMBER: builtins.int
    SYMMETRY_FIELD_NUMBER: builtins.int
    TOPDOWN_FIELD_NUMBER: builtins.int
    AREA_PRICE_FIELD_NUMBER: builtins.int
    FABRICS_FIELD_NUMBER: builtins.int
    DRAPING_MATERIAL_MODEL_FIELD_NUMBER: builtins.int
    DRAPING_UD_COEFFICIENT_FIELD_NUMBER: builtins.int
    DROP_OFF_MATERIAL_HANDLING_FIELD_NUMBER: builtins.int
    DROP_OFF_MATERIAL_FIELD_NUMBER: builtins.int
    CUT_OFF_MATERIAL_HANDLING_FIELD_NUMBER: builtins.int
    CUT_OFF_MATERIAL_FIELD_NUMBER: builtins.int
    THICKNESS_FIELD_NUMBER: builtins.int
    AREA_WEIGHT_FIELD_NUMBER: builtins.int
    status: ansys.api.acp.v0.enum_types_pb2.StatusType.ValueType = ...
    """general properties"""

    symmetry: ansys.api.acp.v0.ply_material_pb2.SymmetryType.ValueType = ...
    topdown: builtins.bool = ...
    """topdown=True: the first fabric in the list is placed first in the mold"""

    area_price: builtins.float = ...
    @property
    def fabrics(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___FabricWithAngle]: ...
    draping_material_model: ansys.api.acp.v0.ply_material_pb2.DrapingMaterialType.ValueType = ...
    """draping"""

    draping_ud_coefficient: builtins.float = ...
    drop_off_material_handling: ansys.api.acp.v0.drop_off_material_pb2.MaterialHandlingType.ValueType = ...
    """solid model options"""

    @property
    def drop_off_material(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    cut_off_material_handling: ansys.api.acp.v0.cut_off_material_pb2.MaterialHandlingType.ValueType = ...
    @property
    def cut_off_material(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    thickness: builtins.float = ...
    """read only properties"""

    area_weight: builtins.float = ...
    def __init__(self,
        *,
        status : ansys.api.acp.v0.enum_types_pb2.StatusType.ValueType = ...,
        symmetry : ansys.api.acp.v0.ply_material_pb2.SymmetryType.ValueType = ...,
        topdown : builtins.bool = ...,
        area_price : builtins.float = ...,
        fabrics : typing.Optional[typing.Iterable[global___FabricWithAngle]] = ...,
        draping_material_model : ansys.api.acp.v0.ply_material_pb2.DrapingMaterialType.ValueType = ...,
        draping_ud_coefficient : builtins.float = ...,
        drop_off_material_handling : ansys.api.acp.v0.drop_off_material_pb2.MaterialHandlingType.ValueType = ...,
        drop_off_material : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        cut_off_material_handling : ansys.api.acp.v0.cut_off_material_pb2.MaterialHandlingType.ValueType = ...,
        cut_off_material : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        thickness : builtins.float = ...,
        area_weight : builtins.float = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["cut_off_material",b"cut_off_material","drop_off_material",b"drop_off_material"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["area_price",b"area_price","area_weight",b"area_weight","cut_off_material",b"cut_off_material","cut_off_material_handling",b"cut_off_material_handling","draping_material_model",b"draping_material_model","draping_ud_coefficient",b"draping_ud_coefficient","drop_off_material",b"drop_off_material","drop_off_material_handling",b"drop_off_material_handling","fabrics",b"fabrics","status",b"status","symmetry",b"symmetry","thickness",b"thickness","topdown",b"topdown"]) -> None: ...
global___Properties = Properties

class ObjectInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    INFO_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    @property
    def info(self) -> ansys.api.acp.v0.base_pb2.BasicInfo: ...
    @property
    def properties(self) -> global___Properties: ...
    def __init__(self,
        *,
        info : typing.Optional[ansys.api.acp.v0.base_pb2.BasicInfo] = ...,
        properties : typing.Optional[global___Properties] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["info",b"info","properties",b"properties"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["info",b"info","properties",b"properties"]) -> None: ...
global___ObjectInfo = ObjectInfo

class ListReply(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    OBJECTS_FIELD_NUMBER: builtins.int
    @property
    def objects(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ObjectInfo]: ...
    def __init__(self,
        *,
        objects : typing.Optional[typing.Iterable[global___ObjectInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["objects",b"objects"]) -> None: ...
global___ListReply = ListReply

class CreateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COLLECTION_PATH_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    @property
    def collection_path(self) -> ansys.api.acp.v0.base_pb2.CollectionPath: ...
    name: typing.Text = ...
    @property
    def properties(self) -> global___Properties: ...
    def __init__(self,
        *,
        collection_path : typing.Optional[ansys.api.acp.v0.base_pb2.CollectionPath] = ...,
        name : typing.Text = ...,
        properties : typing.Optional[global___Properties] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["collection_path",b"collection_path","properties",b"properties"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["collection_path",b"collection_path","name",b"name","properties",b"properties"]) -> None: ...
global___CreateRequest = CreateRequest
