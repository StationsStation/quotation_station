from base_dao import BaseDAO


class QuoteDAO(BaseDAO):
    """QuoteDAO is a class that provides methods to interact with the quote data."""

    def __init__(self):
        super().__init__()
        self.model_name = "quote"
        self.other_model_names = ["RequestForQuote", "CreateRFQ", "RFQError", "Accept"]
