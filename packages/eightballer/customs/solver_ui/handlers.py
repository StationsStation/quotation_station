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

"""This package contains a scaffold of a handler."""

import re
from typing import Optional, cast
from urllib.parse import unquote, urlparse

from aea.skills.base import Handler
from aea.protocols.base import Message
from packages.eightballer.protocols.http.message import HttpMessage as ApiHttpMessage
from .generated.dao.create_r_f_q_dao import CreaterfqDAO


rfq_dao = CreaterfqDAO()


class ApiHttpHandler(Handler):
    """Implements the API HTTP handler."""

    SUPPORTED_PROTOCOL = ApiHttpMessage.protocol_id  # type: Optional[str]

    def setup(self) -> None:
        """Set up the handler."""


    def teardown(self) -> None:
        """Tear down the handler."""

    def handle(self, message: ApiHttpMessage) -> None:
        """Handle incoming API HTTP messages."""
        method = message.method.lower()
        parsed_url = urlparse(unquote(message.url))
        path = parsed_url.path
        body = message.body

        normalized_path = path.rstrip("/")

        normalized_path = re.sub(r"/(\d+)(?=/|$)", "/rfqId", normalized_path)

        handler_name = f"handle_{method}_{normalized_path.lstrip('/').replace('/', '_')}"

        handler_name = handler_name.replace("rfqId", "by_rfqId")

        handler_method = getattr(self, handler_name, None)

        if handler_method:
            kwargs = {"body": body} if method in {"post", "put", "patch", "delete"} else {}

            rfqId_match = re.search(r"/(\d+)(?=/|$)", path)
            if rfqId_match:
                kwargs["rfqId"] = rfqId_match.group(1)

            return handler_method(message, **kwargs)

        return self.handle_unexpected_message(message)

    def handle_post_api_rfq(self, body, message: ApiHttpMessage):
        """Handle POST request for /api/rfq."""
        return rfq_dao.insert(body)

    def handle_get_api_rfq(self, message: ApiHttpMessage):
        """Handle GET request for /api/rfq."""
        return rfq_dao.get_all()

    def handle_post_api_rfq_by_rfqid_accept(self, rfqId, body, message: ApiHttpMessage):
        """Handle POST request for /api/rfq/{rfqId}/accept."""
        # TODO: Implement POST logic for /api/rfq/{rfqId}/accept
        raise NotImplementedError

    def handle_unexpected_message(self, message):
        """Handler for unexpected messages."""
        self.context.logger.info(f"Received unexpected message: {message}")
        raise NotImplementedError
