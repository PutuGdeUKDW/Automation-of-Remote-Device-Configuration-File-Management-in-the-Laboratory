class MikrotikBackupError(Exception):
    def __init__(self, message): 
        super().__init__(message)

class CiscoBackupError(Exception):
    def __init__(self, message): 
        super().__init__(message) 