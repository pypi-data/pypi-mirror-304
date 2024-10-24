"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class DoubleArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    DATA_FIELD_NUMBER: builtins.int
    SHAPE_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    @property
    def shape(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(self,
        *,
        data : typing.Optional[typing.Iterable[builtins.float]] = ...,
        shape : typing.Optional[typing.Iterable[builtins.int]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data","shape",b"shape"]) -> None: ...
global___DoubleArray = DoubleArray

class IntArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    DATA_FIELD_NUMBER: builtins.int
    SHAPE_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def shape(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(self,
        *,
        data : typing.Optional[typing.Iterable[builtins.int]] = ...,
        shape : typing.Optional[typing.Iterable[builtins.int]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data","shape",b"shape"]) -> None: ...
global___IntArray = IntArray

class Int32Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    DATA_FIELD_NUMBER: builtins.int
    SHAPE_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def shape(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(self,
        *,
        data : typing.Optional[typing.Iterable[builtins.int]] = ...,
        shape : typing.Optional[typing.Iterable[builtins.int]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data","shape",b"shape"]) -> None: ...
global___Int32Array = Int32Array
