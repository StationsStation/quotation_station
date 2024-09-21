from base_dao import BaseDAO


class RequestforquoteDAO(BaseDAO):
    """RequestforquoteDAO is a class that provides methods to interact with the requestforquote data."""

    def __init__(self):
        super().__init__()
        self.model_name = "requestforquote"
        self.other_model_names = ["CreateRFQ", "Quote", "RFQError", "Accept"]
