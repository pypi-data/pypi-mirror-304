from enum import Enum, auto

class ResultType(Enum):
    Error = 0
    WaitNext = 1
    Success = 2

class LoginState(Enum):
    WaitLogin = 0
    Login = 1
    WaitOtp = 2
    Success = 3
    Error = 4

class NodeControlState(Enum):
    Continue = 0
    Reset = 1

class PayoutBatchState(Enum):
    Ready = auto()
    UploadedWaitResults = auto()
    CommittedWaitResults = auto()
    Success = auto()
    UploadError = auto()
    CheckError = auto()

class RunningState(Enum):
    Ready = 0
    Running = 1
    Stopped = 2