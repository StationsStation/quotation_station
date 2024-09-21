from base_dao import BaseDAO


class CreaterfqDAO(BaseDAO):
    """CreaterfqDAO is a class that provides methods to interact with the createrfq data."""

    def __init__(self):
        super().__init__()
        self.model_name = "createrfq"
        self.other_model_names = ["RequestForQuote", "Quote", "RFQError", "Accept"]
