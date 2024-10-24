"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import ansys.api.acp.v0.base_pb2
import ansys.api.acp.v0.imported_production_ply_pb2
import grpc

class ObjectServiceStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    List: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.base_pb2.ListRequest,
        ansys.api.acp.v0.imported_production_ply_pb2.ListReply] = ...
    """Object is generated on update and read-only =>
    only list and get endpoints.
    """

    Get: grpc.UnaryUnaryMultiCallable[
        ansys.api.acp.v0.base_pb2.GetRequest,
        ansys.api.acp.v0.imported_production_ply_pb2.ObjectInfo] = ...


class ObjectServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def List(self,
        request: ansys.api.acp.v0.base_pb2.ListRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.imported_production_ply_pb2.ListReply:
        """Object is generated on update and read-only =>
        only list and get endpoints.
        """
        pass

    @abc.abstractmethod
    def Get(self,
        request: ansys.api.acp.v0.base_pb2.GetRequest,
        context: grpc.ServicerContext,
    ) -> ansys.api.acp.v0.imported_production_ply_pb2.ObjectInfo: ...


def add_ObjectServiceServicer_to_server(servicer: ObjectServiceServicer, server: grpc.Server) -> None: ...
