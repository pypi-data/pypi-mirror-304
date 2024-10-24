"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
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
    MATERIAL_FIELD_NUMBER: builtins.int
    THICKNESS_FIELD_NUMBER: builtins.int
    ANGLE_FIELD_NUMBER: builtins.int
    ACTIVE_IN_POST_MODE_FIELD_NUMBER: builtins.int
    status: ansys.api.acp.v0.enum_types_pb2.StatusType.ValueType = ...
    """Object is generated on update and all properties are read only."""

    @property
    def material(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    thickness: builtins.float = ...
    angle: builtins.float = ...
    """angle in degree"""

    active_in_post_mode: builtins.bool = ...
    def __init__(self,
        *,
        status : ansys.api.acp.v0.enum_types_pb2.StatusType.ValueType = ...,
        material : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        thickness : builtins.float = ...,
        angle : builtins.float = ...,
        active_in_post_mode : builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["material",b"material"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["active_in_post_mode",b"active_in_post_mode","angle",b"angle","material",b"material","status",b"status","thickness",b"thickness"]) -> None: ...
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
