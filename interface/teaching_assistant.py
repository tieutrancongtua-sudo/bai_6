from interface.i_borrower import IBorrower 

class TeachingAssistant(IBorrower):
    def __init__(self, borrower_id: str, full_name: str):
        self._borrower_id = borrower_id
        self._full_name = full_name

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def full_name(self) -> str:
        return self._full_name

    def get_maximum_devices(self) -> int:
        return 2