import time
import datetime
import re
from enum import IntEnum


import pymfx4.mfdatastorage as ds
import pymfx4.mfparameters as mfp
import pymfx4.mffullindex as mff
from pymfx4.mfkeyboard import keyboard as kb
from pymfx4 import mfl


class mfx4device:
    """Base class for the MFX_4 devices family.

    Contains wrappers for base function
    - Determining the device class (edi / terminal / controller) and version.
    - reboot device, save parameters, write/read parameters.
    """

    IxCutSaveAllParameter = mff.FullIndex(0, 0x1010, 1)
    IxCutCPUClock = mff.FullIndex(0, 0x200B, 0x11)
    IxUploadBin = mff.FullIndex(0, 0x200B, 16)
    IxUpload = mff.FullIndex(0, 0x200B, 8)
    IxUploadAck = mff.FullIndex(0, 0x200B, 0x07)
    IxUploadState = mff.FullIndex(0, 0x200B, 0x09)
    IxUploadCRC = mff.FullIndex(0, 0x200B, 13)
    IxSetMode = mff.FullIndex(0, 0x200B, 5)

    IxManufacturerDeviceName = mff.FullIndex(0, 0x1008, 0x00)
    IxManufacturerSoftwareVersion = mff.FullIndex(0, 0x100A, 0x00)
    IxManufacturerSoftwareDate = mff.FullIndex(0, 0x100A, 0x01)
    IxManufacturerSoftwareTime = mff.FullIndex(0, 0x100A, 0x02)

    IxStoreParameterSaveAll = mff.FullIndex(0, 0x1010, 0x01)
    IxRestoreDefaultParametersIx = mff.FullIndex(0, 0x1011, 3)

    # device soft reset
    DEVICE_REBOOT = 0x64616F6F
    DEVICE_SAVE_ALL_PARAMETERS = 0x65766173

    def __init__(self, NodeId):
        self._Node = NodeId
        ds.storage.AddGenericDevice(NodeId)
        self.GetInfo()

    def TheNode(self):
        return self._Node

    DeviceName = ds.dsproperty(Address=IxManufacturerDeviceName, NodeId=TheNode)
    SoftwareVersion = ds.dsproperty(Address=IxManufacturerSoftwareVersion, NodeId=TheNode)
    SoftwareDate = ds.dsproperty(Address=IxManufacturerSoftwareDate, NodeId=TheNode)
    SoftwareTime = ds.dsproperty(Address=IxManufacturerSoftwareTime, NodeId=TheNode)

    IxStoreParameterSaveAll = ds.dsproperty(Address=IxStoreParameterSaveAll, NodeId=TheNode)

    def GetInfo(self):
        ds.storage.Get(self.DeviceName)
        time.sleep(0.1)
        ds.storage.Get(self.DeviceName)
        time.sleep(0.1)
        ds.storage.Get(self.SoftwareVersion)
        time.sleep(0.1)
        ds.storage.Get(self.SoftwareDate)
        time.sleep(0.1)
        ds.storage.Get(self.SoftwareTime)
        time.sleep(0.1)

    @property
    def Version(self):
        such = self.SoftwareVersion.Value
        if such is None:
            such = ""
        return list(map(int, re.findall(r'([0-9]+)[.]{0,1}', such, re.M | re.I)))

    @property
    def BuildDate(self):
        software_date = self.SoftwareDate.Value
        software_time = self.SoftwareTime.Value
        if software_time is None:
            software_time = ""
        if software_date is None:
            software_date = ""
        try:
            combine_f1 = datetime.datetime.strptime(software_date.strip(), '%b %d %Y')
            combine_f2 = datetime.datetime.strptime(software_time.strip(), '%H:%M:%S').time()
            return datetime.datetime.combine(combine_f1, combine_f2)
        except Exception as ex:
            pass
        return datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    @property
    def FullVersion(self):
        return (self.Version, self.BuildDate)

    def SaveParameters(self):
        ds.storage.Get(self.SoftwareTime)
        ds.storage.Set(self.IxStoreParameterSaveAll, mfx4device.DEVICE_SAVE_ALL_PARAMETERS)

    def Reboot(self):
        ds.storage.Set(self.IxStoreParameterSaveAll, mfx4device.DEVICE_REBOOT)

    def PC1Reset(self):
        ds.storage.Set(mfx4Controller.IxProcessControlCommand.Node(self.TheNode()), 2)
        time.sleep(8)

    def Set(self, FI, Value):
        ds.storage.Set(FI.Node(self.TheNode()), Value)

    def Get(self, FI):
        FI = FI.Node(self.TheNode())
        ds.storage.Get(FI)
        time.sleep(0.8)
        return ds.storage.GetNative(FI)

    def DeployAndCheckEntrywise(self, package, iter=4):
        if isinstance(package, mfp.mfparameters):
            for i in range(iter):
                if mfp.mfParameterManager.DeployAndCheckEntrywise(package, self):
                    return True
                mfl.info("Check failed! Trying again.")
                time.sleep(1)
        return False

    def DeployAndCheck(self, package, iter=4):
        if isinstance(package, mfp.mfparameters):
            for i in range(iter):
                if mfp.mfParameterManager.DeployAndCheck(package, self):
                    return True
                mfl.info("Check failed! Trying again.")
                time.sleep(1)
        return False

    def __eq__(self, other):
        if not isinstance(other, mfx4device):
            return NotImplemented
        return self == other

    def __repr__(self):
        if self.BuildDate != datetime.datetime(1900, 1, 1, 0, 0, 0, 0):
            return f'{self.SoftwareVersion.Value} - N{self._Node:00} - {self.BuildDate:yyyy-mm-dd HH:MM:SS}'
        return f'{self.SoftwareVersion.Value} - N{self._Node:00}'


class AccessControlLevel_t(IntEnum):
    AccessControl_FactorySettings = 0
    AccessControl_Calibration = 1
    AccessControl_Service = 2
    AccessControl_Manager = 3
    AccessControl_Operator = 4
    AccessControl_None = 7
    AccessControl_Default = AccessControl_None


class mfx4Controller(mfx4device):
    """Represents an MFX_4 Controller V2.

    Used to distinfffguish devices.
    Contains relevant controller CANOpen addresses.
    """

    IxAccessRightsActGroup = mff.FullIndex(0, 0x2820, 0x01)
    IxAccessRightsKey = mff.FullIndex(0, 0x2820, 0x02)
    IxAccessRightsLogin = mff.FullIndex(0, 0x2820, 0x03)
    IxAccessRightsPWService = mff.FullIndex(0, 0x2820, 0x04)
    IxAccessRightsPWManager = mff.FullIndex(0, 0x2820, 0x05)
    IxAccessRightsPWOperator = mff.FullIndex(0, 0x2820, 0x06)
    # IxAccessRightsCalibrationMode = mff.FullIndex(0,0x2820,0x06)

    # Controller specific
    IxProcessControlCommand = mff.FullIndex(0, 0x2425, 11)
    IxProcessControlTransaction = mff.FullIndex(0, 0x2425, 0x0D)
    IxProcessControlBatch = mff.FullIndex(0, 0x2425, 0x0C)
    IxDigitalInputBits = mff.FullIndex(0, 0x2705, 0x0)
    IxDigitalOutputBits = mff.FullIndex(0, 0x2707, 0x0)

    IxPulseAB_Mode = mff.FullIndex(0, 0x21F0, 0x01)
    IxPulseAB_MaxFrequency = mff.FullIndex(0, 0x21F0, 0x04)
    IxPulseAB_Frequency = mff.FullIndex(0, 0x21F0, 0x07)
    IxPulseAB_PulseLost = mff.FullIndex(0, 0x21F0, 0x0A)
    IxPulseAB_PulseRevers = mff.FullIndex(0, 0x21F0, 0x09)
    IxPulseAB_PulseAll = mff.FullIndex(0, 0x21F0, 0x0B)
    IxPulseAB_PulseA = mff.FullIndex(0, 0x21F0, 0x0C)

    IxPulseC_Mode = mff.FullIndex(0, 0x21F1, 0x01)
    IxPulseC_MaxFrequency = mff.FullIndex(0, 0x21F1, 0x04)
    IxPulseC_Frequency = mff.FullIndex(0, 0x21F1, 0x07)
    IxPulseC_Pulse = mff.FullIndex(0, 0x21F1, 0x0C)

    IxPulseD_Mode = mff.FullIndex(0, 0x21F2, 0x01)
    IxPulseD_MaxFrequency = mff.FullIndex(0, 0x21F2, 0x04)
    IxPulseD_Frequency = mff.FullIndex(0, 0x21F2, 0x07)
    IxPulseD_PulseAll = mff.FullIndex(0, 0x21F2, 0x0B)

    IxPressure1_Mode = mff.FullIndex(0, 0x2620, 0x01)
    IxPressure1_PressureLow = mff.FullIndex(0, 0x2620, 0x02)
    IxPressure1_PressureHigh = mff.FullIndex(0, 0x2620, 0x03)
    IxPressure1_AnalogLow = mff.FullIndex(0, 0x2620, 0x04)
    IxPressure1_AnalogHigh = mff.FullIndex(0, 0x2620, 0x05)
    IxPressure1_PressureMinError = mff.FullIndex(0, 0x2620, 0x06)
    IxPressure1_PressureMaxError = mff.FullIndex(0, 0x2620, 0x07)
    IxPressure1_PressureShiftError = mff.FullIndex(0, 0x2620, 0x08)
    IxPressure1_PressureValue = mff.FullIndex(0, 0x2620, 0x09)
    IxPressure2_Mode = mff.FullIndex(0, 0x2621, 0x01)
    IxPressure2_PressureLow = mff.FullIndex(0, 0x2621, 0x02)
    IxPressure2_PressureHigh = mff.FullIndex(0, 0x2621, 0x03)
    IxPressure2_AnalogLow = mff.FullIndex(0, 0x2621, 0x04)
    IxPressure2_AnalogHigh = mff.FullIndex(0, 0x2621, 0x05)
    IxPressure2_PressureMinError = mff.FullIndex(0, 0x2621, 0x06)
    IxPressure2_PressureMaxError = mff.FullIndex(0, 0x2621, 0x07)
    IxPressure2_PressureShiftError = mff.FullIndex(0, 0x2621, 0x08)
    IxPressure2_PressureValue = mff.FullIndex(0, 0x2621, 0x09)

    IxError1_LastError = mff.FullIndex(0, 0x2805, 0x07)
    IxError1_ErrorNo0 = mff.FullIndex(0, 0x2805, 0x09)
    IxError1_ErrorNo1 = mff.FullIndex(0, 0x2805, 0x0A)

    IxExtLog_Blk1 = mff.FullIndex(0, 0x2A40, 0x03)
    IxExtLog_Blk2 = mff.FullIndex(0, 0x2A40, 0x04)
    IxExtLog_Blk3 = mff.FullIndex(0, 0x2A40, 0x05)
    IxExtLog_Blk4 = mff.FullIndex(0, 0x2A40, 0x06)
    IxExtLog_Blk5 = mff.FullIndex(0, 0x2A40, 0x07)
    IxExtLog_Blk6 = mff.FullIndex(0, 0x2A40, 0x08)
    IxExtLog_Blk7 = mff.FullIndex(0, 0x2A40, 0x09)
    IxExtLog_Blk8 = mff.FullIndex(0, 0x2A40, 0x0A)
    IxExtLog_Blk9 = mff.FullIndex(0, 0x2A40, 0x0B)
    IxExtLog_Blk10 = mff.FullIndex(0, 0x2A40, 0x0C)
    IxExtLog_Blk11 = mff.FullIndex(0, 0x2A40, 0x0D)

    ConstAccessControlMultiplier = 0x1000000
    ConstAccessControlFactory = 4712

    def __init__(self, NodeId):
        self._Node = NodeId
        ds.storage.AddGenericDevice(NodeId)
        self.GetInfo()

    def TheNode(self):
        return self._Node


class mfx4Cut(mfx4device):
    """Base class representing representing MFX_4 CUT devices EDI / TERMINAL.

    Used to distinfffguish devices.
    Contains relevant CUT CANOpen addresses.
    """

    IxMeter1State = mff.FullIndex(0, 0x2200, 0x09)

    def __init__(self, NodeId):
        self._Node = NodeId
        ds.storage.AddGenericDevice(NodeId)
        self.GetInfo()

    def TheNode(self):
        return self._Node


class mfx4Terminal(mfx4Cut):

    IxLastKeySimulator = mff.FullIndex(0, 0x2A60, 2)
    IxLastKey = mff.FullIndex(0, 0x200B, 6)

    IxTerminalTerminalInputState = mff.FullIndex(0, 0x2300, 8)
    IxTerminalState = mff.FullIndex(0, 0x2300, 7)
    IxTerminalMeterIndex = mff.FullIndex(0, 0x2300, 9)

    IxBOLConsistency = mff.FullIndex(0, 0x2450, 0x16)
    IxBolPrintingState = mff.FullIndex(0, 0x2450, 0x0A)
    IxBOLPrintingMeter = mff.FullIndex(0, 0x2450, 0x0B)

    IxBOLConsistency = mff.FullIndex(0, 0x2450, 0x16)
    IxBolPrintingState = mff.FullIndex(0, 0x2450, 0x0A)
    IxBOLPrintingMeter = mff.FullIndex(0, 0x2450, 0x0B)

    IxCardreaderMulti1State = mff.FullIndex(0, 0x2090, 0x04)

    IxDisplayObjectCharset = mff.FullIndex(0, 0x2005, 0x0C)

    IxHintTextMode = mff.FullIndex(0, 0x2006, 0x03)
    IxHintTextNumber = mff.FullIndex(0, 0x2006, 0x04)
    IxHintText1 = mff.FullIndex(0, 0x2006, 0x06)
    IxHintText2 = mff.FullIndex(0, 0x2006, 0x07)
    IxHintText3 = mff.FullIndex(0, 0x2006, 0x08)
    IxHintText4 = mff.FullIndex(0, 0x2006, 0x09)
    IxHintText5 = mff.FullIndex(0, 0x2006, 0x0A)
    IxHintText6 = mff.FullIndex(0, 0x2006, 0x0B)
    IxHintText7 = mff.FullIndex(0, 0x2006, 0x0C)
    IxHintText8 = mff.FullIndex(0, 0x2006, 0x0D)
    IxHintText9 = mff.FullIndex(0, 0x2006, 0x0E)
    IxHintText10 = mff.FullIndex(0, 0x2006, 0x0F)

    IxArmDefinition = mff.FullIndex(0, 0x2911, 0x03)

    IxMeterSpecific1DisplayLines = mff.FullIndex(0, 0x2901, 0x0D)

    IxRecipe4 = mff.FullIndex(0, 0x2911, 0x07)
    IxRecipe5 = mff.FullIndex(0, 0x2911, 0x08)

    def __init__(self, NodeId):
        self._Node = NodeId
        ds.storage.AddGenericDevice(NodeId)
        self.GetInfo()

    def TheNode(self):
        return self._Node

    def pressKey(self, key, sleep=1):
        ds.storage.Set(mfx4Terminal.IxLastKeySimulator.Node(self._Node), key)
        time.sleep(sleep)

    def pressKeys(self, keylist):
        for key in keylist:
            self.pressKey(key)

    def pressKeysFast(self, keylist):
        for key in keylist:
            self.pressKey(key, 0.2)

    def DelInput(self):
        for i in range(20):
            self.pressKey(kb.DEL, 0.1)

    def Home(self):
        print("Zurueck zur frmArmliste")
        self.pressKeysFast([kb.F1, kb.F1])

    def PresetArm(self, ArmNr):
        print("Preset Arm " + str(ArmNr))
        self.pressKeysFast([kb.Numbers[ArmNr], kb.F3])
        self.pressKeysFast([kb.Zwei, kb.Null, kb.Null, kb.Null, kb.F4])
        self.pressKeysFast([kb.Eins, kb.F4])
        time.sleep(5)
        self.pressKeysFast([kb.F3])

    def StopArm(self, ArmNr):
        print("Stop Arm " + str(ArmNr))
        self.pressKeysFast([kb.Numbers[ArmNr], kb.F3])

    def PrintArm(self, ArmNr):
        print("Print Arm " + str(ArmNr))
        self.pressKeysFast([kb.Numbers[ArmNr], kb.F2])
        self.pressKey(kb.Numbers[7])


def GetDeviceWithType(deviceType, deviceArray):
    for dev in deviceArray:
        if isinstance(dev, deviceType):
            return dev
    return None
