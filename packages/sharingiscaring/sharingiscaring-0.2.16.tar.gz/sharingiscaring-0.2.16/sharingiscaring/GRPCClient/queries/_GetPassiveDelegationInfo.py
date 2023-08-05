from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from enum import Enum
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from rich import print

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def get_passive_delegation_info(
        self: GRPCClient, block_hash: str
    ) -> CCD_PassiveDelegationInfo:
        prefix = ""
        result = {}
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value: PoolInfoResponse = self.stub.GetPassiveDelegationInfo(
            request=blockHashInput
        )

        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(
                descriptor, grpc_return_value
            )
            key_to_store = f"{prefix}{key}"
            if type(value) in self.simple_types:
                result[key_to_store] = self.convertType(value)

            elif type(value) == CommissionRates:
                result[key] = self.convertCommissionRates(value)

        return CCD_PassiveDelegationInfo(**result)
