class AutomateException(Exception):
    def __init__(self, message: str, inner_exception: Exception = None):
        super().__init__(message)
        self.inner_exception = inner_exception

# exceptions/automate_fatal_exception.py
class AutomateFatalException(Exception):
    pass