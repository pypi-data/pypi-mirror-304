# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ansys.api.acp.v0 import base_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_base__pb2
from ansys.api.acp.v0 import virtual_geometry_pb2 as ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2


class ObjectServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.List = channel.unary_unary(
                '/ansys.api.acp.v0.virtual_geometry.ObjectService/List',
                request_serializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.ListRequest.SerializeToString,
                response_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ListReply.FromString,
                )
        self.Get = channel.unary_unary(
                '/ansys.api.acp.v0.virtual_geometry.ObjectService/Get',
                request_serializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.GetRequest.SerializeToString,
                response_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
                )
        self.Put = channel.unary_unary(
                '/ansys.api.acp.v0.virtual_geometry.ObjectService/Put',
                request_serializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.SerializeToString,
                response_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
                )
        self.Delete = channel.unary_unary(
                '/ansys.api.acp.v0.virtual_geometry.ObjectService/Delete',
                request_serializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.DeleteRequest.SerializeToString,
                response_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.Empty.FromString,
                )
        self.Create = channel.unary_unary(
                '/ansys.api.acp.v0.virtual_geometry.ObjectService/Create',
                request_serializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.CreateRequest.SerializeToString,
                response_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
                )


class ObjectServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def List(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ObjectServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.ListRequest.FromString,
                    response_serializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ListReply.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.GetRequest.FromString,
                    response_serializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.SerializeToString,
            ),
            'Put': grpc.unary_unary_rpc_method_handler(
                    servicer.Put,
                    request_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
                    response_serializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.DeleteRequest.FromString,
                    response_serializer=ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.Empty.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.CreateRequest.FromString,
                    response_serializer=ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ansys.api.acp.v0.virtual_geometry.ObjectService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ObjectService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ansys.api.acp.v0.virtual_geometry.ObjectService/List',
            ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.ListRequest.SerializeToString,
            ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ListReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ansys.api.acp.v0.virtual_geometry.ObjectService/Get',
            ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.GetRequest.SerializeToString,
            ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ansys.api.acp.v0.virtual_geometry.ObjectService/Put',
            ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.SerializeToString,
            ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ansys.api.acp.v0.virtual_geometry.ObjectService/Delete',
            ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.DeleteRequest.SerializeToString,
            ansys_dot_api_dot_acp_dot_v0_dot_base__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ansys.api.acp.v0.virtual_geometry.ObjectService/Create',
            ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.CreateRequest.SerializeToString,
            ansys_dot_api_dot_acp_dot_v0_dot_virtual__geometry__pb2.ObjectInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
