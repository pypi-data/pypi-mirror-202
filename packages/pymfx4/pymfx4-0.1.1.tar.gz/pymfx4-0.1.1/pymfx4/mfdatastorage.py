"""Defines and instanciates the mfDatastorage.

Attributes:
    storage (mfDatastorage): Central piece of CANOpen datamanagement within the pymfx4 package.

Todo:
    * Allow for more than one connection at the same time.
"""

from pymfx4.mffullindex import FullIndex
import pymfx4.mfx4driver as mfx
from pymfx4.mfxdd import genericXDD, cutXDD, controllerXDD
from pymfx4 import mfl
import xml.etree.ElementTree as ET
import base64

# class CanOpenObject(object):
#     """Represents a CANOpen Sub/Object."""

#     def __init__(self, name, objectType, dataType, lowLimit, highLimit, defaultValue, accessType, PDOmapping):
#         self.name = name
#         self.objectType = objectType
#         self.dataType = dataType
#         self.lowLimit = lowLimit
#         self.highLimit = highLimit
#         self.defaultValue = defaultValue
#         self.accessType = accessType
#         self.PDOmapping = PDOmapping


class DatastorageEntry(object):
    """Represents an CANOpen entry."""

    datatype_convert = {
        -1: "c",
        0x01: "c",
        0x02: "c",
        0x03: "i",
        0x04: "I",
        0x05: "C",
        0x06: "I",
        0x07: "L",
        0x08: "F",
        0x09: "S",
        0x0E: "d",
        0x0F: "S",
    }
    # BOOLEAN         = 0x0001,
    # INTEGER8        = 0x0002,
    # INTEGER16       = 0x0003,
    # INTEGER32       = 0x0004,
    # UNSIGNED8       = 0x0005,
    # UNSIGNED16      = 0x0006,
    # UNSIGNED32      = 0x0007,
    # REAL32          = 0x0008,
    # VISIBLE_STRING  = 0x0009,
    # REAL64          = 0x000E, // BIT_STRING, used for double values
    # //reserved        = 0x000E, // official CANopen spec.
    # DOMAIN          = 0x000F,

    NumToTypeFunc = {

        0x01: bool,

        # signed
        0x02: int,
        0x03: int,
        0x04: int,

        # unsigned
        0x05: int,
        0x06: int,
        0x07: int,

        # floating point
        0x08: float,  # float
        0x0E: float,  # double

        0x09: str,
        0x0F: str,
    }

    def __init__(self, function, datatype, fi):
        self.Time = 500
        self.FIndex = fi
        self.OnChangeOnly = False
        self.Function = function
        self.PreviousValue = None
        self.Value = None

        self._dataType = None
        if datatype is not None:
            self._dataType = int(datatype, 16)

        self.DataType = None
        self.DataTypeCAN = None
        if self._dataType is not None and self._dataType in DatastorageEntry.datatype_convert:
            self.DataType = DatastorageEntry.NumToTypeFunc[self._dataType]
            self.DataTypeCAN = DatastorageEntry.datatype_convert[self._dataType]
        else:
            datatype = "None" if datatype is None else datatype
            mfl.warning(f"{__class__} Datatype: '{datatype}' is not valid.")

    def Notify(self, Value):
        self.PreviousValue = self.Value
        self.Value = Value
        changed = self.Value != self.PreviousValue
        if self.Function is not None and ((self.OnChangeOnly and changed) or self.OnChangeOnly is False):
            self.Function(self.FIndex, self.Value)

    def NativeValue(self):
        if self.Value is None or self.DataType is None:
            return None
        if self.DataType == str:
            return self.Value

        return self.DataType(self.Value)


class dsproperty(property):
    """Convenience wrapper for accessing predefined CANOpen-Objects of the datastorage."""

    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.Address = kwargs["Address"]
        self.NodeId = kwargs["NodeId"]

        args2 = (self._get, self._set, self._del, "")
        super(dsproperty, self).__init__(*args2)

    def _get(self, self2):
        no = self.NodeId(self2)
        hey = self.Address.Node(no)
        dff = storage[hey]
        return dff

    def _set(self, self2, value):
        storage[self.Address.Node(self.NodeId(self2))].Value = value

    def _del(self, self2):
        pass

    def GetAddress(self, self2):
        return self.Address.Node(self.NodeId(self2))

    # def Address(self,self2):
    #    return self.Address.Node(self.NodeId(self2))


class mfDatastorage(object):
    """Manages a list of MFX_4 device CANOpen object dictionaries (OD).

    OD are stored in the xdd format as base64 in mfxdd.
    Add device-xdds, read, write, and set notifications. 
    """

    mfx4_devices = {}
    mfx4_devices["generic"] = genericXDD
    mfx4_devices["cut communication unit"] = cutXDD
    mfx4_devices["terminalpro"] = cutXDD
    mfx4_devices["mfx_4 edi"] = cutXDD
    mfx4_devices["modospro"] = cutXDD
    mfx4_devices["mfx_4 controller"] = controllerXDD

    def __init__(self):
        self.Structure = {}
        self.mfc = None

    def AddGenericDevice(self, node):
        self.AddDeviceXdd(node, genericXDD)

    def AddDeviceByName(self, node, devicename):
        if devicename is not None:
            dev = devicename.lower().rstrip('\x00')
            if dev in mfDatastorage.mfx4_devices:
                st = mfDatastorage.mfx4_devices[dev]
                self.AddDeviceXdd(node, st)
                return True
        return False

    def AddDevice(self, dev):
        if dev is not None and dev.DeviceName.Value is not None and dev.SoftwareVersion.Value is not None:
            return self.AddDeviceByName(dev._Node, dev.DeviceName.Value)
        return False

    def AddDeviceXdd(self, node, filename):
        # root = ET.parse(filename).getroot()
        filenametext = base64.b64decode(filename)  # , validate=False)
        root = ET.fromstring(filenametext)
        obj = root.findall('CANopenObject')
        for CANopenObject in obj:
            index = int(CANopenObject.get('index'), 16)
            dataType = CANopenObject.get('dataType')
            subindex = 0
            ind = FullIndex(node, index, subindex)
            if ind not in self.Structure and dataType is not None:
                self.Structure[ind] = DatastorageEntry(self.TheVoid, dataType, ind)
                mfl.debug(f"SUCCESS-TAG: 0x{index:4X}")

            for CANopenSubObject in CANopenObject.findall('CANopenSubObject'):
                dataType2 = CANopenSubObject.get('dataType')
                subindex2 = int(CANopenSubObject.get('subIndex'), 16)
                ind2 = FullIndex(node, index, subindex2)
                if ind2 not in self.Structure and dataType2 is not None:
                    self.Structure[ind2] = DatastorageEntry(self.TheVoid, dataType2, ind2)
                mfl.debug(f"SUCCESS-SUB-TAG: 0x{index:4X} 0x{subindex2:2X}")

        mfl.debug(f"Datastorage: {len(self.Structure)} done")

    def Notify(self, FI, Value):
        if self[FI] is not None:
            self[FI].Notify(Value)
        else:
            mfl.warning(f"{FI} not in Datastorage-Structure")

    def RefreshNotification(self, FI):
        self.mfc.Send(mfx.SetNotification(FI, self[FI].Time))

    def SetNotification(self, FI, time=500, Func=None, OnChangeOnly=False):
        if isinstance(FI, dsproperty) or isinstance(FI, DatastorageEntry):
            FI = FI.FIndex
        self.mfc.Send(mfx.SetNotification(FI, time))
        self[FI].Time = time
        self[FI].OnChangeOnly = OnChangeOnly
        if Func is not None:
            self[FI].Function = Func

    def RemoveNotification(self, FI):
        if isinstance(FI, dsproperty) or isinstance(FI, DatastorageEntry):
            FI = FI.FIndex
        self.mfc.Send(mfx.RemoveNotification(FI))
        self[FI].Function = None

    def Get(self, FI, overrideCANType=None):
        if isinstance(FI, DatastorageEntry):
            FI = FI.FIndex
        if FI.NodeId == 0:
            self.mfc.Send(mfx.ReadObject(FI))
        elif overrideCANType is not None:
            self.mfc.Send(mfx.ReadObjectCan(FI, overrideCANType))
        elif self[FI].DataTypeCAN is not None:
            self.mfc.Send(mfx.ReadObjectCan(FI, self[FI].DataTypeCAN))

        if self[FI] is None:
            return None
        return self.Structure[FI].Value

    def GetNative(self, FI):
        if isinstance(FI, DatastorageEntry):
            FI = FI.FIndex
        if self[FI] is None:
            return None
        return self[FI].NativeValue()

    def Set(self, FI, Value, overrideCANType=None):
        if isinstance(FI, DatastorageEntry):
            FI = FI.FIndex
        if FI.NodeId == 0:
            self.mfc.Send(mfx.WriteObject(FI, Value))
        elif overrideCANType is not None:
            self.mfc.Send(mfx.WriteObjectCan(FI, overrideCANType, Value))
        elif self[FI].DataTypeCAN is not None:
            self.mfc.Send(mfx.WriteObjectCan(FI, self[FI].DataTypeCAN, Value))

    def SetBinary(self, FI, Value):
        self.Set(FI, Value, "b")

    def GetBinary(self, FI):
        return self.Get(FI, "b")

    def TheVoid(self, FI, Value):
        pass

    def __getitem__(self, key):
        if key in self.Structure:
            return self.Structure[key]
        mfl.warning(f"{__class__}; Key {key} not found in Datastorage.")
        return None


# TODO
# The pymfx4 package will only maintain one connection
# with a shared datastorage object defined here.
storage = mfDatastorage()
storage.AddGenericDevice(0)
