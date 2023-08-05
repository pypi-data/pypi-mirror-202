from enum import IntEnum


class TerminalInputState(IntEnum):
    NONE = 0
    Password = 1
    Transaction = 8
    Batch = 10
    Parameter_Item = 20
    Barrels = 37
    License_Plate = 80
    Order_Number = 100
    Unknown = 255


class TerminalDisplayState(IntEnum):
    Startup = 0
    Meterlist = 1
    Loading = 3
    LoadingBlending = 5
    Session = 9
    Parameters = 10
    Clock = 40
    ErrorHistory = 45
    Language = 50
    Splash = 55
    Vouchers = 60
    Unknown = 255


class ProcessControlState(IntEnum):
    Blocked = -2
    NoStateAvailable = -1
    SystemStart = 0
    NoPara = 1
    NotReady = 2
    Idle = 3
    TransactionQuantityInput = 4
    BatchQuantityInput = 5
    VolumeWithoutOrder = 6
    ReadyToStart = 7
    Loading = 8
    Stopped = 9
    TransactionQuantityReached = 10
    LoadingInterrupted = 11
    LoadingAborted = 12
    Printing = 15
    Service = 18
    DataTransfer = 20


class ProcessControlCommand(IntEnum):
    STOP = 0
    START = 1
    RESET = 2
    SET_PRESET = 3
    PART_RESET = 4
    SET_TRANSACTION = 5
    ACK_HOST = 10
    ACK_PRINTER = 11


class BoldataState(IntEnum):
    NONE = 0
    FailedControllerOffline = 0x80
    ReqPart1 = 0x02
    FailedReqPart1CRC = 0x82
    ReqPart2 = 0x03
    FailedReqPart2CRC = 0x83
    ReqPart3 = 0x04
    FailedReqPart3CRC = 0x84
    SanityCheckWithControllerData = 0x06
    FailedSanityCheck = 0x86
    SavingLocalCopy = 0x07
    FailedSavingLocalCopy = 0x87
    FormatLines = 0x08
    FailedFormatLines = 0x88
    BuildBol = 0x09
    FailedBuildBol = 0x89
    AcknowledgeDatatransferInDataTransfer = 0x0B
    FailedAcknowledgeDatatransferInDataTransfer = 0x8B
    Failed = 0x0E,
    FailedWithException = 0xEF,
    Success = 0x01


class CARDREADERSTATE_CANOPEN(IntEnum):
    NoCardDetected = 0
    CardPresentOK = 0x1
    CardPresentBAD = 0x2
    CardPresentBeingProcessed = 0x3
    CardPresentMifareSession = 0x4
    CardPresentMifareAuth = 0x5
    CardPresentMifareReaddata = 0x06
    CardPresentMifareAuthError = 0x7
    CardPresentMifareSessionError = 0x08
