from base_dao import BaseDAO


class AcceptDAO(BaseDAO):
    """AcceptDAO is a class that provides methods to interact with the accept data."""

    def __init__(self):
        super().__init__()
        self.model_name = "accept"
        self.other_model_names = ["RequestForQuote", "CreateRFQ", "Quote", "RFQError"]
