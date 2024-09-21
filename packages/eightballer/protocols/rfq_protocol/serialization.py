# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2024 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Serialization module for rfq_protocol protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage  # type: ignore
from aea.mail.base_pb2 import Message as ProtobufMessage  # type: ignore
from aea.protocols.base import Message  # type: ignore
from aea.protocols.base import Serializer  # type: ignore

from packages.eightballer.protocols.rfq_protocol import rfq_protocol_pb2  # type: ignore
from packages.eightballer.protocols.rfq_protocol.custom_types import (  # type: ignore
    Quote,
    RFQError,
    RequestForQuote,
)
from packages.eightballer.protocols.rfq_protocol.message import (  # type: ignore
    RfqProtocolMessage,
)


class RfqProtocolSerializer(Serializer):
    """Serialization for the 'rfq_protocol' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'RfqProtocol' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(RfqProtocolMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        rfq_protocol_msg = rfq_protocol_pb2.RfqProtocolMessage()  # type: ignore

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == RfqProtocolMessage.Performative.CREATE_RFQ:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Create_Rfq_Performative()  # type: ignore
            rfq = msg.rfq
            RequestForQuote.encode(performative.rfq, rfq)
            rfq_protocol_msg.create_rfq.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.QUOTATION:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Quotation_Performative()  # type: ignore
            rfq = msg.rfq
            RequestForQuote.encode(performative.rfq, rfq)
            quote = msg.quote
            Quote.encode(performative.quote, quote)
            rfq_protocol_msg.quotation.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.RFQ_ERROR:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Rfq_Error_Performative()  # type: ignore
            error_code = msg.error_code
            RFQError.encode(performative.error_code, error_code)
            rfq_protocol_msg.rfq_error.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.ACCEPT:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Accept_Performative()  # type: ignore
            quote = msg.quote
            Quote.encode(performative.quote, quote)
            rfq_protocol_msg.accept.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.DECLINE:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Decline_Performative()  # type: ignore
            quote = msg.quote
            Quote.encode(performative.quote, quote)
            rfq_protocol_msg.decline.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Initiate_Atomic_Swap_Performative()  # type: ignore
            quote = msg.quote
            Quote.encode(performative.quote, quote)
            seller_address = msg.seller_address
            performative.seller_address = seller_address
            swap_id = msg.swap_id
            performative.swap_id = swap_id
            secret_hash = msg.secret_hash
            performative.secret_hash = secret_hash
            secret = msg.secret
            performative.secret = secret
            rfq_protocol_msg.initiate_atomic_swap.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Complete_Atomic_Swap_Performative()  # type: ignore
            swap_id = msg.swap_id
            performative.swap_id = swap_id
            secret = msg.secret
            performative.secret = secret
            rfq_protocol_msg.complete_atomic_swap.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.BUYER_CLAIM:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Buyer_Claim_Performative()  # type: ignore
            secret = msg.secret
            performative.secret = secret
            chain_id = msg.chain_id
            performative.chain_id = chain_id
            rfq_protocol_msg.buyer_claim.CopyFrom(performative)
        elif performative_id == RfqProtocolMessage.Performative.SELLER_CLAIM:
            performative = rfq_protocol_pb2.RfqProtocolMessage.Seller_Claim_Performative()  # type: ignore
            secret = msg.secret
            performative.secret = secret
            chain_id = msg.chain_id
            performative.chain_id = chain_id
            rfq_protocol_msg.seller_claim.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = rfq_protocol_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'RfqProtocol' message.

        :param obj: the bytes object.
        :return: the 'RfqProtocol' message.
        """
        message_pb = ProtobufMessage()
        rfq_protocol_pb = rfq_protocol_pb2.RfqProtocolMessage()  # type: ignore
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        rfq_protocol_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = rfq_protocol_pb.WhichOneof("performative")
        performative_id = RfqProtocolMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == RfqProtocolMessage.Performative.CREATE_RFQ:
            pb2_rfq = rfq_protocol_pb.create_rfq.rfq
            rfq = RequestForQuote.decode(pb2_rfq)
            performative_content["rfq"] = rfq
        elif performative_id == RfqProtocolMessage.Performative.QUOTATION:
            pb2_rfq = rfq_protocol_pb.quotation.rfq
            rfq = RequestForQuote.decode(pb2_rfq)
            performative_content["rfq"] = rfq
            pb2_quote = rfq_protocol_pb.quotation.quote
            quote = Quote.decode(pb2_quote)
            performative_content["quote"] = quote
        elif performative_id == RfqProtocolMessage.Performative.RFQ_ERROR:
            pb2_error_code = rfq_protocol_pb.rfq_error.error_code
            error_code = RFQError.decode(pb2_error_code)
            performative_content["error_code"] = error_code
        elif performative_id == RfqProtocolMessage.Performative.ACCEPT:
            pb2_quote = rfq_protocol_pb.accept.quote
            quote = Quote.decode(pb2_quote)
            performative_content["quote"] = quote
        elif performative_id == RfqProtocolMessage.Performative.DECLINE:
            pb2_quote = rfq_protocol_pb.decline.quote
            quote = Quote.decode(pb2_quote)
            performative_content["quote"] = quote
        elif performative_id == RfqProtocolMessage.Performative.INITIATE_ATOMIC_SWAP:
            pb2_quote = rfq_protocol_pb.initiate_atomic_swap.quote
            quote = Quote.decode(pb2_quote)
            performative_content["quote"] = quote
            seller_address = rfq_protocol_pb.initiate_atomic_swap.seller_address
            performative_content["seller_address"] = seller_address
            swap_id = rfq_protocol_pb.initiate_atomic_swap.swap_id
            performative_content["swap_id"] = swap_id
            secret_hash = rfq_protocol_pb.initiate_atomic_swap.secret_hash
            performative_content["secret_hash"] = secret_hash
            secret = rfq_protocol_pb.initiate_atomic_swap.secret
            performative_content["secret"] = secret
        elif performative_id == RfqProtocolMessage.Performative.COMPLETE_ATOMIC_SWAP:
            swap_id = rfq_protocol_pb.complete_atomic_swap.swap_id
            performative_content["swap_id"] = swap_id
            secret = rfq_protocol_pb.complete_atomic_swap.secret
            performative_content["secret"] = secret
        elif performative_id == RfqProtocolMessage.Performative.BUYER_CLAIM:
            secret = rfq_protocol_pb.buyer_claim.secret
            performative_content["secret"] = secret
            chain_id = rfq_protocol_pb.buyer_claim.chain_id
            performative_content["chain_id"] = chain_id
        elif performative_id == RfqProtocolMessage.Performative.SELLER_CLAIM:
            secret = rfq_protocol_pb.seller_claim.secret
            performative_content["secret"] = secret
            chain_id = rfq_protocol_pb.seller_claim.chain_id
            performative_content["chain_id"] = chain_id
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return RfqProtocolMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
