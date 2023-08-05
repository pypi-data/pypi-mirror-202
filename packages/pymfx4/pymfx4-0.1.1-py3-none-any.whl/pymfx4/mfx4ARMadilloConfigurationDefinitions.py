from pymfx4.mfx4ARMadilloEnums import CModuleEnum
from pymfx4.mfx4ARMadilloEnums import CLogEnum
from pymfx4.mfx4ARMadilloEnums import CInternalADCEnum
from pymfx4.mfx4ARMadilloEnums import CSystemEnum
from pymfx4.mfx4ARMadilloEnums import CClockEnum
from pymfx4.mfx4ARMadilloEnums import CAccessControlEnum
from pymfx4.mfx4ARMadilloEnums import CWatchdogEnum

from pymfx4.mfx4ARMadilloEnums import CADConverterEnum
from pymfx4.mfx4ARMadilloEnums import CDAConverterEnum

from pymfx4.mfx4ARMadilloEnums import CPIDControlEnum
from pymfx4.mfx4ARMadilloEnums import CTemperatureEnum
from pymfx4.mfx4ARMadilloEnums import CCounterEnum

from pymfx4.mfx4ARMadilloEnums import CBoardDisplayEnum

from pymfx4.mfx4ARMadilloEnums import CBoardRelayEnum
from pymfx4.mfx4ARMadilloEnums import CBoardDigitalInputEnum
from pymfx4.mfx4ARMadilloEnums import CBoardDigitalOutputEnum
from pymfx4.mfx4ARMadilloEnums import CBoardImpulseEnum
from pymfx4.mfx4ARMadilloEnums import CPulseGeneratorEnum
from pymfx4.mfx4ARMadilloEnums import CSerialEnum

from pymfx4.mfx4ARMadilloEnums import CProcessControlEnum
from pymfx4.mfx4ARMadilloEnums import CProtocolMFX4Enum
from pymfx4.mfx4ARMadilloEnums import CMMemoryEnum
from pymfx4.mfx4ARMadilloEnums import CDensityEnum
from pymfx4.mfx4ARMadilloEnums import CPressureEnum

from pymfx4.mfx4ARMadilloEnums import CErrorEnum
from pymfx4.mfx4ARMadilloEnums import CPulseEnum
from pymfx4.mfx4ARMadilloEnums import CWMHistoryEnum
from pymfx4.mfx4ARMadilloEnums import CProductEnum
from pymfx4.mfx4ARMadilloEnums import CVoucherEnum

from enum import IntEnum
import struct
import jsonpickle


class CMemoryLocations:
    """Important memory locations.

    Synchronize with ARMadillo project!
    """

    W25R_SECTOR_SIZE = 4096
    xFLASH_COPY_COUNT = 2
    xPARAMETER_MAX_SIZE = 8 * W25R_SECTOR_SIZE
    xLINKAGE_MAX_SIZE = 8 * W25R_SECTOR_SIZE
    xModuleAccessMap_MAX_SIZE = 8 * W25R_SECTOR_SIZE
    xModuleQuantityMap_MAX_SIZE = W25R_SECTOR_SIZE

    xConfigurationRAMBufferSize = 8 * W25R_SECTOR_SIZE

    xFlashParameterLocation = 0
    xFlashParameterSize = xFLASH_COPY_COUNT * xPARAMETER_MAX_SIZE
    xFlashParameterSingleSize = xPARAMETER_MAX_SIZE

    xFlashModuleLinkageLocation = xFlashParameterLocation + xFlashParameterSize
    xFlashModuleLinkageSize = xLINKAGE_MAX_SIZE

    xFlashModuleAccessLocation = xFlashModuleLinkageLocation + xFlashModuleLinkageSize
    xFlashModulAccessSize = xModuleAccessMap_MAX_SIZE

    xFlashModuleQuantityLocation = xFlashModuleAccessLocation + xFlashModulAccessSize
    xFlashModuleQuantitySize = xModuleQuantityMap_MAX_SIZE

    xFlashSystemLogsLocation = xFlashModuleQuantityLocation + xFlashModuleQuantitySize
    xFlashSystemLogsSize = 4 * W25R_SECTOR_SIZE

    xFlashLogsLocation = xFlashSystemLogsLocation + xFlashSystemLogsSize
    xFlashLogsSize = 16 * W25R_SECTOR_SIZE

    xFlashCounterProductLinkageLocation = xFlashLogsLocation + xFlashLogsSize
    xFlashCounterProductLinkageSize = W25R_SECTOR_SIZE

    xFlashProductProcessControlLinkageLocation = xFlashCounterProductLinkageLocation + xFlashCounterProductLinkageSize
    xFlashProductProcessControlLinkageSize = W25R_SECTOR_SIZE

    ulVoucherSlotSize = 1024
    ulVoucherSlots = 8
    xFlashVoucherLocation = 0x400000
    xFlashVoucherSize = ulVoucherSlots * ulVoucherSlotSize


ModuleToValues = {
    CModuleEnum.TYPE_LOG: CLogEnum,
    CModuleEnum.TYPE_INTERNAL_ADC: CInternalADCEnum,
    CModuleEnum.TYPE_SYSTEM: CSystemEnum,
    CModuleEnum.TYPE_CLOCK: CClockEnum,
    CModuleEnum.TYPE_ACCESSCONTROL: CAccessControlEnum,
    CModuleEnum.TYPE_WATCHDOG: CWatchdogEnum,

    CModuleEnum.TYPE_ADCONVERTER: CADConverterEnum,
    CModuleEnum.TYPE_DACONVERTER: CDAConverterEnum,

    CModuleEnum.TYPE_PIDCONTROL: CPIDControlEnum,
    CModuleEnum.TYPE_TEMPERATURE: CTemperatureEnum,
    CModuleEnum.TYPE_COUNTER: CCounterEnum,

    CModuleEnum.TYPE_BOARDDISPLAY: CBoardDisplayEnum,

    CModuleEnum.TYPE_BOARDRELAY: CBoardRelayEnum,
    CModuleEnum.TYPE_BOARDDIGITALINPUT: CBoardDigitalInputEnum,
    CModuleEnum.TYPE_BOARDDIGITALOUTPUT: CBoardDigitalOutputEnum,
    CModuleEnum.TYPE_BOARDIMPULSE: CBoardImpulseEnum,
    CModuleEnum.TYPE_PULSEGENERATOR: CPulseGeneratorEnum,
    CModuleEnum.TYPE_SERIAL: CSerialEnum,

    CModuleEnum.TYPE_PROCESSCONTROL: CProcessControlEnum,
    CModuleEnum.TYPE_PROTOCOL_MFX4: CProtocolMFX4Enum,
    CModuleEnum.TYPE_MEMORY_INTERFACE: CMMemoryEnum,
    CModuleEnum.TYPE_DENSITY: CDensityEnum,
    CModuleEnum.TYPE_PRESSURE: CPressureEnum,

    CModuleEnum.TYPE_ERROR: CErrorEnum,
    CModuleEnum.TYPE_PULSE: CPulseEnum,
    CModuleEnum.TYPE_WEIGHT_AND_MEASUREMENT_HISTORY: CWMHistoryEnum,
    CModuleEnum.TYPE_PRODUCT: CProductEnum,
    CModuleEnum.TYPE_VOUCHER: CVoucherEnum,
}


class commonHeader_t:
    """A header class that is common for most ARMadillo configurations.

    Imported class. Binary representation used in the ARMadillo.
    These types of configuration are using the commonHeader_t class: QuantityMap, AccessMap, LinkageMap.
    The header includes a field for the size of the whole configuration.
    """

    def __init__(self):
        self.ulLabel = 0
        self.ucCopyId = 0
        self.usOverallChecksum = 0
        self.ulTotalByteCount = 0

    def GetxNON_CRC_BYTES(self):
        """This many bytes need to be skipped for the crc calculation."""
        return 7

    def usCalculateCRC(self):
        return commonHeader_t.crc_calc(0, self.Pack())

    def xCheckCRC(self):
        return self.usOverallChecksum == self.usCalculateCRC()

    def vCalculateAndSetCRC(self):
        self.usOverallChecksum = self.usCalculateCRC()

    def crc_calc(crc, data):
        crc &= 0xffff

        header = commonHeader_t()
        header.Unpack(data)

        # uint16_t
        usTable = [0] * 256

        for i in range(0, 256):
            k = 0xC0C1
            usTable[i] = 0
            for j in [1, 2, 4, 8, 16, 32, 64, 128]:
                if (i & j) > 0:
                    usTable[i] ^= k
                    usTable[i] &= 0xffff
                k = ((k << 1) ^ 0x4003)

        dat = data[header.GetxNON_CRC_BYTES():header.ulTotalByteCount]
        for p in dat:
            crc = (crc >> 8) ^ usTable[(crc & 0xFF) ^ p]

        return crc

    def Pack(self):
        return struct.pack('<IBHI', self.ulLabel, self.ucCopyId, self.usOverallChecksum, self.ulTotalByteCount)

    def Unpack(self, data):
        d = data[:11]
        self.ulLabel, self.ucCopyId, self.usOverallChecksum, self.ulTotalByteCount = struct.unpack('<IBHI', d)

    def __repr__(self):
        options = {moduleAccessMapHeader_t.ulMODULE_ACCESS_MAP_LABEL: "Module Access Map",
                   moduleLinkageHeader_t.ulMODULE_LINKAGE_LABEL: "Module Linkage Map",
                   moduleQuantityHeader_t.ulMODULE_QUANTITY_LABEL: "Module Quantity Map"}
        header = "Configuration?"
        if self.ulLabel in options.keys():
            header = options[self.ulLabel]
        header = f"{header} ({self.ucCopyId})\n"
        header += f"CRC: 0x{self.usOverallChecksum:X}\n"
        header += f"Bytes: {self.ulTotalByteCount}\n"

        return f'{header}'


class moduleId_t:
    """Representing a ARMadillo module with module type and sequence number.

    Imported class. Binary representation used in the ARMadillo.
    """

    def G(usSeqNumArg, xTypeArg):
        a = moduleId_t()
        a.usSeqNum = usSeqNumArg
        try:
            a.xType = CModuleEnum(xTypeArg)
        except:
            a.xType = CModuleEnum.TYPE_MAX
        return a

    def __init__(self):
        self.usSeqNum = 0
        self.xType = CModuleEnum.TYPE_MAX

    def __repr__(self):
        usSeq = f'{self.usSeqNum:02d}'
        if self.usSeqNum == 0xffff:
            usSeq = "?"

        xT = f'{self.xType:02d}'
        name = self.xType.name
        if int(self.xType) == 0xff:
            xT = "?"
            name = "?"

        return f'[{usSeq}][{xT}] {name}'

    def Pack(self):
        return struct.pack('<HH', self.usSeqNum, self.xType)


class uniqueValueId_t:
    """Representing an address to a ARMadillo-modules value-container.

    Imported class. Binary representation used in the ARMadillo.
    """

    def G(xModuleIdArg, xValueIdArg):
        a = uniqueValueId_t()
        a.xModuleId = xModuleIdArg
        a.xValueId = xValueIdArg
        return a

    def __init__(self):
        self.xModuleId = 0
        self.xValueId = 0

    def Pack(self):
        return self.xModuleId.Pack() + struct.pack('<H', self.xValueId)

    def Unpack(self, data):
        d = data[:6]
        a, b, self.xValueId, = struct.unpack('<HHH', d)
        self.xModuleId = moduleId_t.G(a, b)

    def __repr__(self):
        ret = f'*{self.xValueId}'
        if self.xModuleId.xType in ModuleToValues.keys():
            values = [item.value for item in ModuleToValues[self.xModuleId.xType]]
            if self.xValueId in values:
                ret = ModuleToValues[self.xModuleId.xType](self.xValueId)
                ret = f'{ret.name} *{ret.value}'

        return f'{self.xModuleId}=={ret}'


class moduleConfigurationHeader:
    """Base class of most ARMadillo configrations.

    Imported class. Binary representation used in the ARMadillo.
    Helper functions include import and export.
    """

    def __init__(self):
        self.xCommonHeader = commonHeader_t()

    def Prepare(self):
        self.xCommonHeader.ulTotalByteCount = len(self.Pack())
        self.xCommonHeader.usOverallChecksum = commonHeader_t.crc_calc(0, self.Pack())
        pass

    def Export(obj, filePath=None):
        jsondata = jsonpickle.encode(obj, make_refs=False, indent=3)

        import os
        namespace = "pymfx4." + os.path.basename(__file__).replace(".py", "")

        jsondata = jsondata.replace("__main__", namespace)

        # jsondata = pickle.dumps(obj)
        if filePath:
            try:
                with open(filePath, 'wt') as f:
                    f.write(jsondata)
            except:
                pass
        return jsondata

    def Import(filePath=None, data=None):
        if filePath:
            with open(filePath, 'rt') as f:
                data = f.read()
        if data:
            return jsonpickle.decode(data, safe=True)  # , classes=[moduleQuantityHeader_t, moduleQuantity_t, CModuleEnum])
        return None


class moduleLinkageHeader_t(moduleConfigurationHeader):
    """Module linkage ARMadillo configuration.

    Imported class. Binary representation used in the ARMadillo.
    """

    ulMODULE_LINKAGE_LABEL = 0x4D4C0000

    def __init__(self):
        super().__init__()
        self.xCommonHeader.ulLabel = moduleLinkageHeader_t.ulMODULE_LINKAGE_LABEL
        self.ulModuleLinkageMappingCount = 0
        self.xMappings = []
        self.Prepare()

    def Pack(self):
        ret = self.xCommonHeader.Pack() + struct.pack('<I', self.ulModuleLinkageMappingCount)
        for m in self.xMappings:
            ret += m.Pack()
        return ret

    def Unpack(self, data):
        self.xCommonHeader.Unpack(data)
        d = data[11:15]
        self.ulModuleLinkageMappingCount, = struct.unpack('<I', d)
        d = data[15:]
        for i in range(self.ulModuleLinkageMappingCount):
            mapping = moduleLinkageMapping_t()
            mapping.Unpack(d)
            self.xMappings.append(mapping)
            d = d[7 + mapping.xConsumerCount * 6:]

    def __repr__(self):
        ret = f'{self.xCommonHeader}'
        for i in self.xMappings:
            ret += f"{i}"
        return ret

    def Sort(self):
        # def index(elem):
        #     return elem.xProducerId.xModuleId.xType
        # self.xMappings.sort(key=index)

        self.xMappings.sort(key=lambda x: x.xProducerId.xModuleId.xType)

    def Prepare(self):
        self.ulModuleLinkageMappingCount = len(self.xMappings)
        super().Prepare()
        pass


class moduleLinkageMapping_t:
    """Module linkage ARMadillo configuration content.

    Imported class. Binary representation used in the ARMadillo.
    """

    def G(xProducerIdArg, *pxConsumerIds):
        a = moduleLinkageMapping_t()
        a.xConsumerCount = len(pxConsumerIds)
        a.xProducerId = xProducerIdArg

        a.pxConsumerIds = []
        for arg in pxConsumerIds:
            a.pxConsumerIds.append(arg)
        return a

    def __init__(self):
        self.xConsumerCount = 0
        self.xProducerId = 0
        self.pxConsumerIds = []

    def Pack(self):
        ret = struct.pack('<B', self.xConsumerCount)
        ret += self.xProducerId.Pack()
        for ids in self.pxConsumerIds:
            ret += ids.Pack()
        return ret

    def Unpack(self, data):
        self.xConsumerCount, = struct.unpack('<B', data[0:1])
        self.xProducerId = uniqueValueId_t()
        self.xProducerId.Unpack(data[1:7])
        for i in range(self.xConsumerCount):
            uVId = uniqueValueId_t()
            uVId.Unpack(data[7 + (i * 6):7 + (i * 6 + 6)])
            self.pxConsumerIds.append(uVId)

    def __repr__(self):
        ret = f'{self.xProducerId} =>\n'
        for i in self.pxConsumerIds:
            ret += f'\t{i}\n'
        return ret


class moduleAccessMapHeader_t(moduleConfigurationHeader):
    """Module access ARMadillo configuration.

    Imported class. Binary representation used in the ARMadillo.
    """

    ulMODULE_ACCESS_MAP_LABEL = 0x434f494d

    def __init__(self):
        super().__init__()
        self.xCommonHeader.ulLabel = moduleAccessMapHeader_t.ulMODULE_ACCESS_MAP_LABEL
        self.moduleAccessObjects = []
        self.Prepare()

    def Unpack(self, data):
        self.xCommonHeader.Unpack(data)
        d = data[11:]
        parsed = 11
        while parsed < self.xCommonHeader.ulTotalByteCount:
            obj = moduleAccessObjectHeader_t()
            obj.usIndex, obj.ucSubCount, = struct.unpack('<HB', d[:3])

            d = d[3:]
            parsed += 3
            for i in range(obj.ucSubCount + 1):
                sub = moduleAccessSubObject_t()
                sub.Unpack(d)
                obj.pxSubObjects.append(sub)
                d = d[11:]
                parsed += 11

            self.moduleAccessObjects.append(obj)

    def Pack(self):
        ret = self.xCommonHeader.Pack()
        for m in self.moduleAccessObjects:
            ret += m.Pack()
        return ret

    def __repr__(self):
        ret = f'{self.xCommonHeader}'

        total = 0
        for i in self.moduleAccessObjects:
            total += len(i.pxSubObjects)

        ret += f'Total SubObjects: {total}\n'

        for i in self.moduleAccessObjects:
            ret += f'\t{i}'
        return ret

    def Prepare(self):
        for i in self.moduleAccessObjects:
            i.ucSubCount = len(i.pxSubObjects) - 1
            if len(i.pxSubObjects) - 1 < 0:
                i.ucSubCount = 0
        self.Sort()
        super().Prepare()
        pass

    def Sort(self):
        # self.moduleAccessObjects.sort(key=index)
        # self.moduleAccessObjects.sort(key=lambda x: x.usIndex)
        for i in self.moduleAccessObjects:
            # i.pxSubObjects.sort(key=subindex)
            # i.pxSubObjects.sort(key=lambda x: x.xUniqueValueId.xValueId)
            i.pxSubObjects.sort(key=lambda x: x.ucSubIndex)
            i.ucSubCount = len(i.pxSubObjects) - 1
            if i.ucSubCount < 0:
                i.ucSubCount = 0


class moduleAccessObjectHeader_t:
    """Module access ARMadillo configuration content.

    Imported class. Binary representation used in the ARMadillo.
    """

    def __init__(self):
        self.usIndex = 0
        self.ucSubCount = 0
        self.pxSubObjects = []

    def __repr__(self):
        ret = f'Object 0x{self.usIndex:X} (Count:{self.ucSubCount})\n'
        for i in self.pxSubObjects:
            ret += f'\t\t{i}\n'
        return ret

    def Pack(self):
        ret = struct.pack('<HB', self.usIndex, self.ucSubCount)
        for m in self.pxSubObjects:
            ret += m.Pack()
        return ret


class moduleAccessSubObject_t:
    """Module access ARMadillo configuration content.

    Imported class. Binary representation used in the ARMadillo.
    """

    def __init__(self):
        self.ucSubIndex = 0
        self.usByteCount = 0
        self.xUniqueValueId = uniqueValueId_t()
        self.ucFlags = 0
        self.eMFXType = 0  # byte

    def Unpack(self, data):
        self.ucSubIndex, self.usByteCount, = struct.unpack('<BH', data[:3])
        self.xUniqueValueId.Unpack(data[3:])
        self.ucFlags, self.eMFXType, = struct.unpack('<BB', data[9:11])

    def Pack(self):
        ret = struct.pack('<BH', self.ucSubIndex, self.usByteCount)
        ret += self.xUniqueValueId.Pack()
        ret += struct.pack('<BB', self.ucFlags, self.eMFXType)
        return ret

    def __repr__(self):
        return f"{self.xUniqueValueId} (Sub:0x{self.ucSubIndex:X}/{self.ucSubIndex}) (Bytes:{self.usByteCount})"


class moduleQuantityHeader_t(moduleConfigurationHeader):
    """Module quantity ARMadillo configuration content.

    Imported class. Binary representation used in the ARMadillo.
    """

    ulMODULE_QUANTITY_LABEL = 0x514d0000

    def __init__(self):
        super().__init__()
        self.xCommonHeader.ulLabel = moduleQuantityHeader_t.ulMODULE_QUANTITY_LABEL
        self.usModuleCount = 0
        self.pxModuleQuantities = []
        self.Prepare()

    def Unpack(self, data):
        self.xCommonHeader.Unpack(data)
        d = data[11:]
        self.usModuleCount, = struct.unpack('<H', d[:2])
        d = d[2:]
        for i in range(self.usModuleCount):
            obj = moduleQuantity_t()
            obj.Unpack(d[:4])
            self.pxModuleQuantities.append(obj)
            d = d[4:]

    def Pack(self):
        ret = self.xCommonHeader.Pack()
        ret += struct.pack("<H", self.usModuleCount)
        for m in self.pxModuleQuantities:
            ret += m.Pack()
        return ret

    def __repr__(self):
        ret = f'{self.xCommonHeader}'
        ret += f'Entries: {self.usModuleCount}\n'
        for i in self.pxModuleQuantities:
            ret += f'\t{i}\n'
        return ret

    def Sort(self):
        self.pxModuleQuantities.sort(key=lambda x: x.xModuleType)
        super().Prepare()

    def Prepare(self):
        self.Sort()
        self.usModuleCount = len(self.pxModuleQuantities)
        super().Prepare()
        pass


class moduleQuantity_t:
    """Module quantity ARMadillo configuration content.

    Imported class. Binary representation used in the ARMadillo.
    """
    def G(xModuleType, usModuleQuantity):
        quan = moduleQuantity_t()
        quan.xModuleType = xModuleType
        quan.usModuleQuantity = usModuleQuantity
        return quan

    def __init__(self):
        self.xModuleType = CModuleEnum.TYPE_MAX
        self.usModuleQuantity = 0

    def Unpack(self, data):
        a, self.usModuleQuantity = struct.unpack('<HH', data[:4])
        values = set(item.value for item in CModuleEnum)
        if a in values:
            self.xModuleType = CModuleEnum(a)

    def Pack(self):
        return struct.pack('<HH', self.xModuleType, self.usModuleQuantity)

    def __repr__(self):
        return f"{self.xModuleType.name}: {self.usModuleQuantity}"


class logSeverity_t(IntEnum):
    """Severity of reported log content.

    Imported class. Binary representation used in the ARMadillo.
    """

    NOMASK = 0x30,
    ERROR = 0x31
    WARNING = 0x32
    HINT = 0x33


class logMessage_t:
    """Representation of an ARMadillo log message .

    Imported class. Binary representation used in the ARMadillo.
    """

    LOG_MAX_SOURCEFILE_LEN = 10
    LOG_MAX_COMMENT_LEN = 37

    def __init__(self):
        self.xTimestamp = 0  # 8byte
        self.xSeverity = logSeverity_t.NOMASK.value  # 1byte
        self.xModuleId = moduleId_t()
        self.pcSourceFile = ""  # LOG_MAX_SOURCEFILE_LEN
        self.usLineNumber = 0  # 2byte
        self.usCause = 0   # 2byte
        self.pcComment = ""  # LOG_MAX_COMMENT_LEN

    def Unpack(self, data):
        self.xTimestamp, self.xSeverity, a, b, self.pcSourceFile, self.usLineNumber, self.usCause, self.pcComment = struct.unpack(f'<QBHH{logMessage_t.LOG_MAX_SOURCEFILE_LEN}sHH{logMessage_t.LOG_MAX_COMMENT_LEN}s', data[:64])
        self.xModuleId = moduleId_t.G(a, b)

    def Pack(self):
        ret = struct.pack('<QB', self.xTimestamp, self.xSeverity)
        ret += self.xModuleId.Pack()
        sourceFileString = f"{self.pcSourceFile:<{logMessage_t.LOG_MAX_SOURCEFILE_LEN}}"
        if len(sourceFileString) > logMessage_t.LOG_MAX_SOURCEFILE_LEN:
            sourceFileString = sourceFileString[0:logMessage_t.LOG_MAX_SOURCEFILE_LEN]
        ret += struct.pack(f'<{logMessage_t.LOG_MAX_SOURCEFILE_LEN}sHH', bytes(sourceFileString, encoding="ASCII"), self.usLineNumber, self.usCause)

        comment = f"{self.pcComment:<{logMessage_t.LOG_MAX_COMMENT_LEN}}"
        if len(comment) > logMessage_t.LOG_MAX_COMMENT_LEN:
            comment = comment[0:logMessage_t.LOG_MAX_COMMENT_LEN]
        ret += struct.pack('<{logMessage_t.LOG_MAX_COMMENT_LEN}s', bytes(comment, encoding="ASCII"))
        return ret

    def __repr__(self):
        a = self.pcSourceFile.encode("ascii")
        b = self.pcComment.encode("ascii")
        return f"{self.xTimestamp :<10} {self.xModuleId}: {a} {b}"


class ErrorConfiguration_t:
    """Representation of an ARMadillo error configuration.
    
    Imported class. Binary representation used in the ARMadillo.
    [todo]
    """

    ERROR_NO_BIT = 0
    ERROR_NO_VALUE = 0x7FF << ERROR_NO_BIT
    ERRORLESS_PART_GENERATION_BIT = 11
    ERRORLESS_PART_GENERATION_VALUE = 0x1 << ERRORLESS_PART_GENERATION_BIT
    CAUSES_BIT = 12
    CAUSES_VALUE = 0x7 << CAUSES_BIT
    RESET_BY_COMMAND_BIT = 15
    RESET_BY_COMMAND_VALUE = 0x1 << 15
    DELAY_BREAK_TIME_BIT = 16
    DELAY_BREAK_TIME_VALUE = 0xFFF << DELAY_BREAK_TIME_BIT
    OUTPUT_BIT = 28
    OUTPUT_VALUE = 0xf << OUTPUT_BIT

    def __init__(self):
        self.ulErrorProperties = 0  # 4byte
        self.ulPermissionProperties = 0  # 4byte
        self.ulProcessControls = 0  # 4byte

    def Unpack(self, data):
        self.ulErrorProperties, self.ulPermissionProperties, self.ulProcessControls = struct.unpack('<III', data[:12])

    def Pack(self):
        ret = struct.pack('<III', self.ulErrorProperties, self.ulPermissionProperties, self.ulProcessControls)
        return ret

    def __repr__(self):
        # ErrorClass = (self.ulErrorProperties & ErrorConfiguration_t.ERROR_NO_VALUE) >> ErrorConfiguration_t.ERROR_NO_BIT
        # Cause = (self.ulErrorProperties & ErrorConfiguration_t.CAUSES_VALUE) >> ErrorConfiguration_t.CAUSES_BIT
        # ResetCommand = (self.ulErrorProperties & ErrorConfiguration_t.RESET_BY_COMMAND_VALUE) >> ErrorConfiguration_t.RESET_BY_COMMAND_BIT
        # DelayBreakTime = (self.ulErrorProperties & ErrorConfiguration_t.DELAY_BREAK_TIME_VALUE) >> ErrorConfiguration_t.DELAY_BREAK_TIME_BIT
        # Output = (self.ulErrorProperties & ErrorConfiguration_t.OUTPUT_VALUE) >> ErrorConfiguration_t.OUTPUT_BIT

        return f"EC{self.ErrorClass:<5} F{self.GenerateErrorlessPart} C{self.Cause} RES{self.ResetCommand} DELAY{self.DelayBreakTime} OUT{self.Output}"

    @property
    def GenerateErrorlessPart(self):
        return (self.ulErrorProperties & ErrorConfiguration_t.ERRORLESS_PART_GENERATION_VALUE) >> ErrorConfiguration_t.ERRORLESS_PART_GENERATION_BIT

    @GenerateErrorlessPart.setter
    def GenerateErrorlessPart(self, x):
        self.ulErrorProperties &= ~ErrorConfiguration_t.ERRORLESS_PART_GENERATION_VALUE
        x = x & (ErrorConfiguration_t.ERRORLESS_PART_GENERATION_VALUE >> ErrorConfiguration_t.ERRORLESS_PART_GENERATION_BIT)
        self.ulErrorProperties |= x << ErrorConfiguration_t.ERRORLESS_PART_GENERATION_BIT

    @property
    def Output(self):
        return (self.ulErrorProperties & ErrorConfiguration_t.OUTPUT_VALUE) >> ErrorConfiguration_t.OUTPUT_BIT

    @Output.setter
    def Output(self, x):
        self.ulErrorProperties &= ~ErrorConfiguration_t.OUTPUT_VALUE
        x = x & (ErrorConfiguration_t.OUTPUT_VALUE >> ErrorConfiguration_t.OUTPUT_BIT)
        self.ulErrorProperties |= x << ErrorConfiguration_t.OUTPUT_BIT

    @property
    def DelayBreakTime(self):
        return (self.ulErrorProperties & ErrorConfiguration_t.DELAY_BREAK_TIME_VALUE) >> ErrorConfiguration_t.DELAY_BREAK_TIME_BIT

    @DelayBreakTime.setter
    def DelayBreakTime(self, x):
        self.ulErrorProperties &= ~ErrorConfiguration_t.DELAY_BREAK_TIME_VALUE
        x = x & (ErrorConfiguration_t.DELAY_BREAK_TIME_VALUE >> ErrorConfiguration_t.DELAY_BREAK_TIME_BIT)
        self.ulErrorProperties |= x << ErrorConfiguration_t.DELAY_BREAK_TIME_BIT

    @property
    def ResetCommand(self):
        return (self.ulErrorProperties & ErrorConfiguration_t.RESET_BY_COMMAND_VALUE) >> ErrorConfiguration_t.RESET_BY_COMMAND_BIT

    @ResetCommand.setter
    def ResetCommand(self, x):
        self.ulErrorProperties &= ~ErrorConfiguration_t.RESET_BY_COMMAND_VALUE
        x = x & (ErrorConfiguration_t.RESET_BY_COMMAND_VALUE >> ErrorConfiguration_t.RESET_BY_COMMAND_BIT)
        self.ulErrorProperties |= x << ErrorConfiguration_t.RESET_BY_COMMAND_BIT

    @property
    def Cause(self):
        return (self.ulErrorProperties & ErrorConfiguration_t.CAUSES_VALUE) >> ErrorConfiguration_t.CAUSES_BIT

    @Cause.setter
    def Cause(self, x):
        self.ulErrorProperties &= ~ErrorConfiguration_t.CAUSES_VALUE
        x = x & (ErrorConfiguration_t.CAUSES_VALUE >> ErrorConfiguration_t.CAUSES_BIT)
        self.ulErrorProperties |= x << ErrorConfiguration_t.CAUSES_BIT

    @property
    def ErrorClass(self):
        return (self.ulErrorProperties & ErrorConfiguration_t.ERROR_NO_VALUE) >> ErrorConfiguration_t.ERROR_NO_BIT

    @ErrorClass.setter
    def ErrorClass(self, x):
        self.ulErrorProperties &= ~ErrorConfiguration_t.ERROR_NO_VALUE
        x = x & (ErrorConfiguration_t.ERROR_NO_VALUE >> ErrorConfiguration_t.ERROR_NO_BIT)
        self.ulErrorProperties |= x << ErrorConfiguration_t.ERROR_NO_BIT
