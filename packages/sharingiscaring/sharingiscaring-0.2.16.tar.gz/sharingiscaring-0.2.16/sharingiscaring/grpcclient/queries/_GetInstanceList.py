from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import Iterator
from typing import TYPE_CHECKING
import sys

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def get_instance_list(self: GRPCClient, block_hash: str) -> list[CCD_BakerId]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value: Iterator[ContractAddress] = self.stub.GetInstanceList(
            request=blockHashInput
        )

        for instance in list(grpc_return_value):

            result.append(self.convertType(instance))

        return result
