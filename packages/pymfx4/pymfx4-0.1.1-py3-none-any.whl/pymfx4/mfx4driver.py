from pymfx4.mffullindex import FullIndex

"""MFX_4 Protocol wrappers.

Read, Write, Re/setNotification.
"""

def LCRWrapper(func):
    """Old format with bbc."""
    def wrapper(*args, **kwargs):
        st = func(*args, **kwargs)
        byt = f"{chr(2)}0{st}{chr(3)}"
        checksum = 2
        for b in byt:
            checksum ^= ord(b)
        checksum = checksum % 128
        if checksum < 0x20:
            checksum += 0x40
        byt = byt + chr(checksum)
        return byt
    return wrapper


def WriteObject(fIndex, data):
    fIndex.NodeId = 0
    return f"WO_{0}_{fIndex.Index}_{fIndex.SubIndex}_{data}`"


def ReadObject(fIndex):
    fIndex.NodeId = 0
    return f"RO_{fIndex.NodeId}_{fIndex.Index}_{fIndex.SubIndex}`"


def WriteObjectCan(fIndex, datatype, data):
    return f"WC_{fIndex.NodeId}_{fIndex.Index}_{fIndex.SubIndex}_{datatype}_{data}`"


def ReadObjectCan(fIndex, datatype):
    return f"RC_{fIndex.NodeId}_{fIndex.Index}_{fIndex.SubIndex}_{datatype}`"


def SetNotification(fIndex: FullIndex, time=500):
    if fIndex.NodeId > 0:
        return f"SM_{fIndex.NodeId}_{fIndex.Index}_{fIndex.SubIndex}_{time}`"
    else:
        return f"SN_{fIndex.Index}_{fIndex.SubIndex}_{time}`"


def RemoveNotification(fIndex: FullIndex):
    if fIndex.NodeId > 0:
        return f"CM_{fIndex.NodeId}_{fIndex.Index}_{fIndex.SubIndex}`"
    else:
        return f"CN_{fIndex.Index}_{fIndex.SubIndex}`"
