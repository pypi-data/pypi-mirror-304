"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import ansys.api.acp.v0.array_types_pb2
import ansys.api.acp.v0.base_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class _ElementalDataType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ElementalDataTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ElementalDataType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
    ELEMENT_COORDINATES: ElementalDataType.ValueType = ...  # 0
    ELEMENT_NORMAL: ElementalDataType.ValueType = ...  # 1
    ELEMENT_ORIENTATION: ElementalDataType.ValueType = ...  # 2
    ELEMENT_REFERENCE_DIRECTION: ElementalDataType.ValueType = ...  # 3
    ELEMENT_FIBER_DIRECTION: ElementalDataType.ValueType = ...  # 4
    ELEMENT_DRAPED_FIBER_DIRECTION: ElementalDataType.ValueType = ...  # 5
    ELEMENT_TRANSVERSE_DIRECTION: ElementalDataType.ValueType = ...  # 6
    ELEMENT_DRAPED_TRANSVERSE_DIRECTION: ElementalDataType.ValueType = ...  # 7
    ELEMENT_THICKNESS: ElementalDataType.ValueType = ...  # 8
    ELEMENT_RELATIVE_THICKNESS_CORRECTION: ElementalDataType.ValueType = ...  # 9
    ELEMENT_DESIGN_ANGLE: ElementalDataType.ValueType = ...  # 10
    ELEMENT_SHEAR_ANGLE: ElementalDataType.ValueType = ...  # 11
    ELEMENT_DRAPED_FIBER_ANGLE: ElementalDataType.ValueType = ...  # 12
    ELEMENT_DRAPED_TRANSVERSE_ANGLE: ElementalDataType.ValueType = ...  # 13
    ELEMENT_AREA: ElementalDataType.ValueType = ...  # 14
    ELEMENT_PRICE: ElementalDataType.ValueType = ...  # 15
    ELEMENT_VOLUME: ElementalDataType.ValueType = ...  # 16
    ELEMENT_MASS: ElementalDataType.ValueType = ...  # 17
    ELEMENT_OFFSET: ElementalDataType.ValueType = ...  # 18
    ELEMENT_MATERIAL_1_DIRECTION: ElementalDataType.ValueType = ...  # 19
    ELEMENT_COG: ElementalDataType.ValueType = ...  # 20
    """NOTE dgresch July '23: The elemental ply offset query currently returns
    the ply offset in absolute coordinates, instead of relative to the
    element. Since this is inconsistent with the nodal ply_offset, this query
    is currently disabled. ELEMENT_PLY_OFFSET = 21;
    """

class ElementalDataType(_ElementalDataType, metaclass=_ElementalDataTypeEnumTypeWrapper):
    pass

ELEMENT_COORDINATES: ElementalDataType.ValueType = ...  # 0
ELEMENT_NORMAL: ElementalDataType.ValueType = ...  # 1
ELEMENT_ORIENTATION: ElementalDataType.ValueType = ...  # 2
ELEMENT_REFERENCE_DIRECTION: ElementalDataType.ValueType = ...  # 3
ELEMENT_FIBER_DIRECTION: ElementalDataType.ValueType = ...  # 4
ELEMENT_DRAPED_FIBER_DIRECTION: ElementalDataType.ValueType = ...  # 5
ELEMENT_TRANSVERSE_DIRECTION: ElementalDataType.ValueType = ...  # 6
ELEMENT_DRAPED_TRANSVERSE_DIRECTION: ElementalDataType.ValueType = ...  # 7
ELEMENT_THICKNESS: ElementalDataType.ValueType = ...  # 8
ELEMENT_RELATIVE_THICKNESS_CORRECTION: ElementalDataType.ValueType = ...  # 9
ELEMENT_DESIGN_ANGLE: ElementalDataType.ValueType = ...  # 10
ELEMENT_SHEAR_ANGLE: ElementalDataType.ValueType = ...  # 11
ELEMENT_DRAPED_FIBER_ANGLE: ElementalDataType.ValueType = ...  # 12
ELEMENT_DRAPED_TRANSVERSE_ANGLE: ElementalDataType.ValueType = ...  # 13
ELEMENT_AREA: ElementalDataType.ValueType = ...  # 14
ELEMENT_PRICE: ElementalDataType.ValueType = ...  # 15
ELEMENT_VOLUME: ElementalDataType.ValueType = ...  # 16
ELEMENT_MASS: ElementalDataType.ValueType = ...  # 17
ELEMENT_OFFSET: ElementalDataType.ValueType = ...  # 18
ELEMENT_MATERIAL_1_DIRECTION: ElementalDataType.ValueType = ...  # 19
ELEMENT_COG: ElementalDataType.ValueType = ...  # 20
"""NOTE dgresch July '23: The elemental ply offset query currently returns
the ply offset in absolute coordinates, instead of relative to the
element. Since this is inconsistent with the nodal ply_offset, this query
is currently disabled. ELEMENT_PLY_OFFSET = 21;
"""

global___ElementalDataType = ElementalDataType


class _ElementScopingType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ElementScopingTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ElementScopingType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
    ALL: ElementScopingType.ValueType = ...  # 0
    SHELL: ElementScopingType.ValueType = ...  # 1
    SOLID: ElementScopingType.ValueType = ...  # 2
class ElementScopingType(_ElementScopingType, metaclass=_ElementScopingTypeEnumTypeWrapper):
    pass

ALL: ElementScopingType.ValueType = ...  # 0
SHELL: ElementScopingType.ValueType = ...  # 1
SOLID: ElementScopingType.ValueType = ...  # 2
global___ElementScopingType = ElementScopingType


class _NodalDataType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _NodalDataTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_NodalDataType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
    NODE_PLY_OFFSET: NodalDataType.ValueType = ...  # 0
class NodalDataType(_NodalDataType, metaclass=_NodalDataTypeEnumTypeWrapper):
    pass

NODE_PLY_OFFSET: NodalDataType.ValueType = ...  # 0
global___NodalDataType = NodalDataType


class DataArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    DOUBLE_ARRAY_FIELD_NUMBER: builtins.int
    INT_ARRAY_FIELD_NUMBER: builtins.int
    INT32_ARRAY_FIELD_NUMBER: builtins.int
    @property
    def double_array(self) -> ansys.api.acp.v0.array_types_pb2.DoubleArray: ...
    @property
    def int_array(self) -> ansys.api.acp.v0.array_types_pb2.IntArray: ...
    @property
    def int32_array(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    def __init__(self,
        *,
        double_array : typing.Optional[ansys.api.acp.v0.array_types_pb2.DoubleArray] = ...,
        int_array : typing.Optional[ansys.api.acp.v0.array_types_pb2.IntArray] = ...,
        int32_array : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["data",b"data","double_array",b"double_array","int32_array",b"int32_array","int_array",b"int_array"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data","double_array",b"double_array","int32_array",b"int32_array","int_array",b"int_array"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["data",b"data"]) -> typing.Optional[typing_extensions.Literal["double_array","int_array","int32_array"]]: ...
global___DataArray = DataArray

class MeshData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    NODE_LABELS_FIELD_NUMBER: builtins.int
    NODE_COORDINATES_FIELD_NUMBER: builtins.int
    ELEMENT_LABELS_FIELD_NUMBER: builtins.int
    ELEMENT_TYPES_FIELD_NUMBER: builtins.int
    ELEMENT_NODES_FIELD_NUMBER: builtins.int
    ELEMENT_NODES_OFFSETS_FIELD_NUMBER: builtins.int
    @property
    def node_labels(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    @property
    def node_coordinates(self) -> ansys.api.acp.v0.array_types_pb2.DoubleArray: ...
    @property
    def element_labels(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    @property
    def element_types(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    @property
    def element_nodes(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    @property
    def element_nodes_offsets(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    def __init__(self,
        *,
        node_labels : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        node_coordinates : typing.Optional[ansys.api.acp.v0.array_types_pb2.DoubleArray] = ...,
        element_labels : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        element_types : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        element_nodes : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        element_nodes_offsets : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["element_labels",b"element_labels","element_nodes",b"element_nodes","element_nodes_offsets",b"element_nodes_offsets","element_types",b"element_types","node_coordinates",b"node_coordinates","node_labels",b"node_labels"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["element_labels",b"element_labels","element_nodes",b"element_nodes","element_nodes_offsets",b"element_nodes_offsets","element_types",b"element_types","node_coordinates",b"node_coordinates","node_labels",b"node_labels"]) -> None: ...
global___MeshData = MeshData

class GetElementalDataRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    RESOURCE_PATH_FIELD_NUMBER: builtins.int
    DATA_TYPES_FIELD_NUMBER: builtins.int
    ELEMENT_SCOPING_FIELD_NUMBER: builtins.int
    @property
    def resource_path(self) -> ansys.api.acp.v0.base_pb2.ResourcePath:
        """The resource path determines both the entity whose data is being queried,
        as well as the scope for the elements.
        For example, if the resource path is models/<uuid>, then the data will be
        returned for all elements in the model.
        If the resource path represents a Modeling Ply, the scope will be limited
        to the elements in the ply, and the element data corresponding to the
        ply will be returned.
        """
        pass
    @property
    def data_types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___ElementalDataType.ValueType]: ...
    element_scoping: global___ElementScopingType.ValueType = ...
    """optionally scope by element type"""

    def __init__(self,
        *,
        resource_path : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        data_types : typing.Optional[typing.Iterable[global___ElementalDataType.ValueType]] = ...,
        element_scoping : global___ElementScopingType.ValueType = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_path",b"resource_path"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data_types",b"data_types","element_scoping",b"element_scoping","resource_path",b"resource_path"]) -> None: ...
global___GetElementalDataRequest = GetElementalDataRequest

class ElementalData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    LABELS_FIELD_NUMBER: builtins.int
    DATA_TYPES_FIELD_NUMBER: builtins.int
    DATA_ARRAYS_FIELD_NUMBER: builtins.int
    @property
    def labels(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    @property
    def data_types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___ElementalDataType.ValueType]: ...
    @property
    def data_arrays(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DataArray]: ...
    def __init__(self,
        *,
        labels : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        data_types : typing.Optional[typing.Iterable[global___ElementalDataType.ValueType]] = ...,
        data_arrays : typing.Optional[typing.Iterable[global___DataArray]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["labels",b"labels"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data_arrays",b"data_arrays","data_types",b"data_types","labels",b"labels"]) -> None: ...
global___ElementalData = ElementalData

class GetNodalDataRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    RESOURCE_PATH_FIELD_NUMBER: builtins.int
    DATA_TYPES_FIELD_NUMBER: builtins.int
    ELEMENT_SCOPING_FIELD_NUMBER: builtins.int
    @property
    def resource_path(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    @property
    def data_types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___NodalDataType.ValueType]: ...
    element_scoping: global___ElementScopingType.ValueType = ...
    """optionally scope by element type"""

    def __init__(self,
        *,
        resource_path : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        data_types : typing.Optional[typing.Iterable[global___NodalDataType.ValueType]] = ...,
        element_scoping : global___ElementScopingType.ValueType = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_path",b"resource_path"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data_types",b"data_types","element_scoping",b"element_scoping","resource_path",b"resource_path"]) -> None: ...
global___GetNodalDataRequest = GetNodalDataRequest

class GetMeshDataRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    RESOURCE_PATH_FIELD_NUMBER: builtins.int
    ELEMENT_SCOPING_FIELD_NUMBER: builtins.int
    @property
    def resource_path(self) -> ansys.api.acp.v0.base_pb2.ResourcePath: ...
    element_scoping: global___ElementScopingType.ValueType = ...
    def __init__(self,
        *,
        resource_path : typing.Optional[ansys.api.acp.v0.base_pb2.ResourcePath] = ...,
        element_scoping : global___ElementScopingType.ValueType = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["resource_path",b"resource_path"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["element_scoping",b"element_scoping","resource_path",b"resource_path"]) -> None: ...
global___GetMeshDataRequest = GetMeshDataRequest

class NodalData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    LABELS_FIELD_NUMBER: builtins.int
    DATA_TYPES_FIELD_NUMBER: builtins.int
    DATA_ARRAYS_FIELD_NUMBER: builtins.int
    @property
    def labels(self) -> ansys.api.acp.v0.array_types_pb2.Int32Array: ...
    @property
    def data_types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___NodalDataType.ValueType]: ...
    @property
    def data_arrays(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DataArray]: ...
    def __init__(self,
        *,
        labels : typing.Optional[ansys.api.acp.v0.array_types_pb2.Int32Array] = ...,
        data_types : typing.Optional[typing.Iterable[global___NodalDataType.ValueType]] = ...,
        data_arrays : typing.Optional[typing.Iterable[global___DataArray]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["labels",b"labels"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["data_arrays",b"data_arrays","data_types",b"data_types","labels",b"labels"]) -> None: ...
global___NodalData = NodalData
