"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import ansys.api.acp.v0.base_pb2
import ansys.api.acp.v0.layup_mapping_object_pb2
import grpc

class ObjectServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    List: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.base_pb2.ListRequest,
        ansys.api.acp.v0.layup_mapping_object_pb2.ListReply] = ...

    Get: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.base_pb2.GetRequest,
        ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo] = ...

    Put: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo,
        ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo] = ...

    Delete: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.base_pb2.DeleteRequest,
        ansys.api.acp.v0.base_pb2.Empty] = ...

    Create: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.layup_mapping_object_pb2.CreateRequest,
        ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo] = ...


class ObjectServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def List(self,
        request: ansys.api.acp.v0.base_pb2.ListRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.layup_mapping_object_pb2.ListReply: ...

    @abc.abstractmethod
    def Get(self,
        request: ansys.api.acp.v0.base_pb2.GetRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo: ...

    @abc.abstractmethod
    def Put(self,
        request: ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo: ...

    @abc.abstractmethod
    def Delete(self,
        request: ansys.api.acp.v0.base_pb2.DeleteRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.base_pb2.Empty: ...

    @abc.abstractmethod
    def Create(self,
        request: ansys.api.acp.v0.layup_mapping_object_pb2.CreateRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.layup_mapping_object_pb2.ObjectInfo: ...


def add_ObjectServiceServicer_to_server(servicer: ObjectServiceServicer, server: grpc.Server) -> None: ...
