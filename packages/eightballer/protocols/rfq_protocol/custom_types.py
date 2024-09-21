"""This module contains class representations corresponding to every custom type in the protocol specification."""

from enum import Enum
from typing import Any

from pydantic import BaseModel


class BaseCustomEncoder(BaseModel):
    """
    This class is a base class for encoding and decoding protocol buffer objects.
    """

    @staticmethod
    def encode(ps_response_protobuf_object, ps_response_object) -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the ps_response_protobuf_object argument is matched with the instance of this
        class in the 'ps_response_object' argument.

        :param ps_response_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param ps_response_object: an instance of this class to be encoded in the protocol buffer object.
        """
        for key, value in ps_response_object.__dict__.items():
            current_attr = getattr(ps_response_protobuf_object, key)
            if isinstance(value, Enum):
                type(value).encode(current_attr, value)
                continue
            if isinstance(value, dict):
                current_attr.update(value)
                continue
            if isinstance(value, list):
                current_attr.extend(value)
                continue
            setattr(ps_response_protobuf_object, key, value)

    @classmethod
    def decode(cls, ps_response_protobuf_object) -> "Any":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'ps_response_protobuf_object' argument.

        :param ps_response_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the
        'ps_response_protobuf_object' argument.
        """
        keywords = [f for f in cls.__annotations__.keys()]
        kwargs = {}
        for keyword in keywords:
            proto_attr = getattr(ps_response_protobuf_object, keyword)
            if isinstance(proto_attr, Enum):
                kwargs[keyword] = type(proto_attr).decode(proto_attr)
                continue
            if isinstance(proto_attr, list):
                kwargs[keyword] = [type(proto_attr[0]).decode(item) for item in proto_attr]
                continue
            if isinstance(proto_attr, dict):
                kwargs[keyword] = {k: v for (k, v) in proto_attr.items()}
                continue
            if str(type(proto_attr)) in CUSTOM_ENUM_MAP:
                kwargs[keyword] = CUSTOM_ENUM_MAP[str(type(proto_attr))].decode(proto_attr).value
                continue
            kwargs[keyword] = proto_attr
        return cls(**kwargs)

    def __eq__(self, other):
        """Check if two instances of this class are equal."""
        return self.dict() == other.dict()

    def __hash__(self):
        """Return the hash value of this instance."""
        return hash(self.dict())


class Quote(BaseCustomEncoder):
    """This class represents an instance of Quote."""

    amount_out: int
    bid_token_id: str
    ask_token_id: str
    seller_wallet_address: str
    chain_id: str


class RFQError(Enum):
    """This class represents an instance of RFQError."""

    UNSUPPORTED_TOKEN = 0
    UNSUPPORTED_CHAIN = 1
    NO_QUOTES = 2

    @staticmethod
    def encode(r_f_q_error_protobuf_object, r_f_q_error_object: "RFQError") -> None:
        """
        Encode an instance of this class into the protocol buffer object.

        The protocol buffer object in the r_f_q_error_protobuf_object argument is matched with the instance of this
        class in the 'r_f_q_error_object' argument.

        :param r_f_q_error_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :param r_f_q_error_object: an instance of this class to be encoded in the protocol buffer object.
        """
        r_f_q_error_protobuf_object.r_f_q_error = r_f_q_error_object.value

    @classmethod
    def decode(cls, r_f_q_error_protobuf_object) -> "RFQError":
        """
        Decode a protocol buffer object that corresponds with this class into an instance of this class.

        A new instance of this class is created that matches the protocol buffer object in the
        'r_f_q_error_protobuf_object' argument.

        :param r_f_q_error_protobuf_object: the protocol buffer object whose type corresponds with this class.
        :return: A new instance of this class that matches the protocol buffer object in the
        'r_f_q_error_protobuf_object' argument.
        """
        return RFQError(r_f_q_error_protobuf_object.r_f_q_error)


class RequestForQuote(BaseCustomEncoder):
    """This class represents an instance of RequestForQuote."""

    amount_in: int
    bid_token_id: str
    ask_token_id: str
    buyer_wallet_address: str
    chain_id: str
    expiration_time: int


CUSTOM_ENUM_MAP = {"<class 'rfq_protocol_pb2.RFQError'>": RFQError}
