class BankAutomation:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, cls):
        if not hasattr(cls, '_bank_names'):
            cls._bank_names = []
        cls._bank_names.append(self.name)
        return cls