from base_dao import BaseDAO


class RfqerrorDAO(BaseDAO):
    """RfqerrorDAO is a class that provides methods to interact with the rfqerror data."""

    def __init__(self):
        super().__init__()
        self.model_name = "rfqerror"
        self.other_model_names = ["RequestForQuote", "CreateRFQ", "Quote", "Accept"]
