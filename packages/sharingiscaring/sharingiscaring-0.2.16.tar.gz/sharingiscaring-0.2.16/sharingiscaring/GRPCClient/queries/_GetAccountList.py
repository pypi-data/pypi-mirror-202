from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import Iterator
import sys
from sharingiscaring.GRPCClient.CCD_Types import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient


class Mixin(_SharedConverters):
    def get_account_list(self: GRPCClient, block_hash: str) -> list[CCD_AccountAddress]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value: Iterator[AccountAddress] = self.stub.GetAccountList(
            request=blockHashInput
        )

        for account in list(grpc_return_value):

            result.append(self.convertType(account))

        return result
