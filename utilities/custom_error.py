class CustomError(Exception):
    def __init__(self, error_message, error_code):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_message)


class RegexMismatch(CustomError):
    """Regex Pattern Mismatch"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE01")


class NoContent(CustomError):
    """No Content retrieved from the database"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE02")


class DBDataExtraction(CustomError):
    """Error occurred while extracting data from the database"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE03")


class InvalidRequest(CustomError):
    """Input JSON Request doesn't contain the required parameters"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE04")


class InvalidInputValues(CustomError):
    """Input values doesn't match the standards"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE05")


class VerseIdOutOfRange(CustomError):
    """Verse ID is out of the defined range"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE06")


class InputMissing(CustomError):
    """No Input request provided"""
    def __init__(self, message):
        super().__init__(error_message=message, error_code="DSE07")
