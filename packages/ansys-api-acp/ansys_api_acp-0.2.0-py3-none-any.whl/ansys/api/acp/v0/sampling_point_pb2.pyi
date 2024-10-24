"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import ansys.api.acp.v0.array_types_pb2
import ansys.api.acp.v0.base_pb2
import ansys.api.acp.v0.enum_types_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Properties(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    STATUS_FIELD_NUMBER: builtins.int
    LOCKED_FIELD_NUMBER: builtins.int
    POINT_FIELD_NUMBER: builtins.int
    DIRECTION_FIELD_NUMBER: builtins.int
    USE_DEFAULT_REFERENCE_DIRECTION_FIELD_NUMBER: builtins.int
    ROSETTE_FIELD_NUMBER: builtins.int
    REFERENCE_DIRECTION_FIELD_NUMBER: builtins.int
    OFFSET_IS_MIDDLE_FIELD_NUMBER: builtins.int
    CONSIDER_COUPLING_EFFECT_FIELD_NUMBER: builtins.int
    status: ansys.api.acp.v0.enum_types_pb2.StatusType.ValueType = ...
    """general properties"""

    locked: builtins.bool = ...
    """read-only"""

    @property
    def point(self) -> ansys.api.acp.v0.array_types_pb2.DoubleArray: ...
    @property
    def direction(self) -> ansys.api.acp.v0.array_types_pb2.DoubleArray: ...
    use_default_reference_direction: builtins.bool = ...
    """CLT properties"""

    @property
    def rosette(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    @property
    def reference_direction(self) -> ansys.api.acp.v0.array_types_pb2.DoubleArray:
        """read-only"""
        pass
    offset_is_middle: builtins.bool = ...
    consider_coupling_effect: builtins.bool = ...
    def __init__(self,
        *,
        status : ansys.api.acp.v0.enum_types_pb2.StatusType.ValueType = ...,
        locked : builtins.bool = ...,
        point : typing.Optional[ansys.api.acp.v0.array_types_pb2.DoubleArray] = ...,
        direction : typing.Optional[ansys.api.acp.v0.array_types_pb2.DoubleArray] = ...,
        use_default_reference_direction : builtins.bool = ...,
        rosette : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        reference_direction : typing.Optional[ansys.api.acp.v0.array_types_pb2.DoubleArray] = ...,
        offset_is_middle : builtins.bool = ...,
        consider_coupling_effect : builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["direction",b"direction","point",b"point","reference_direction",b"reference_direction","rosette",b"rosette"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["consider_coupling_effect",b"consider_coupling_effect","direction",b"direction","locked",b"locked","offset_is_middle",b"offset_is_middle","point",b"point","reference_direction",b"reference_direction","rosette",b"rosette","status",b"status","use_default_reference_direction",b"use_default_reference_direction"]) -> None: ...
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
