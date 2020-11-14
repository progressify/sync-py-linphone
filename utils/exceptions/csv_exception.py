
class CsvException(Exception):
    exit_code = 1

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
