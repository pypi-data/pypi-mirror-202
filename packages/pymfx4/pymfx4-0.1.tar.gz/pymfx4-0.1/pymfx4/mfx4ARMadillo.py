import logging
import time
import collections.abc
import binascii
import enum

from pymfx4.mffullindex import FullIndex
from pymfx4.mfx4device import mfx4Controller
import pymfx4.mfdatastorage as ds
import pymfx4.mfx4ARMadilloEnums as mfAE

from pymfx4.mfx4ARMadilloConfigurationDefinitions import commonHeader_t
from pymfx4.mfx4ARMadilloConfigurationDefinitions import CMemoryLocations
from pymfx4.mfx4ARMadilloConfigurationDefinitions import moduleAccessMapHeader_t
from pymfx4.mfx4ARMadilloConfigurationDefinitions import moduleLinkageHeader_t
from pymfx4.mfx4ARMadilloConfigurationDefinitions import moduleQuantityHeader_t
from pymfx4 import mfl


class mfx4ExceptionElevationNeeded(Exception):
    pass

class mfx4ExceptionSystemIsNotResponsive(Exception):
    pass


class memoryOperationEnum(enum.IntEnum):
    """ARMadillo CANOpen Object 0x2010 interface operation.

    The operation that is to be done.
    When writting the data is first written entirely (todo) into 
    a  ram section in the ARMadillo (max 32 KiB), then with a
    RAM_TO_SECTION command it is commited to the section and address
    it belongs to.
    """

    MEMORY_OPERATION_READ = 0
    MEMORY_OPERATION_WRITE_RAM = 1
    MEMORY_OPERATION_WRITE_RAM_TO_SECTION = 2
    MEMORY_OPERATION_ERASE = 4
    MEMORY_OPERATION_MAX = 255


class memorySectionEnum(enum.IntEnum):
    """ARMadillo CANOpen Object 0x2010 interface section."""

    MEMORY_SECTION_CPU_QSPI_FLASH = 0
    MEMORY_SECTION_AIO_I2C_EEPROM = 1
    MEMORY_SECTION_CPU_I2C_EEPROM = 2
    MEMORY_SECTION_MAX = 255


class memoryErrorEnum(enum.IntEnum):
    """Info (and errors) send back from the ARMadillo CANOpen Object 0x2010 interface."""

    MEMORY_ERR_NONE = 0
    MEMORY_ERR_NONE_READ_SUCCESS = 0
    MEMORY_ERR_NONE_WRITE_TO_RAM_SUCCESS = 10
    MEMORY_ERR_NONE_WRITE_RAM_TO_SECTION_SUCCESS = 11
    MEMORY_ERR_ACCESS_DENIED = 1  # insufficient accessrights on the ARMadillo. You need at least 'service'
    MEMORY_ERR_MAX_LENGTH_EXCEEDED = 2  # trying to read/write more than 256 bytes at time.
    MEMORY_ERR_READ = 3
    MEMORY_ERR_WRITE = 5
    MEMORY_ERR_WRITE_TWO_CHARACTERS_PER_BYTE = 6  # Uneven amount of hex-coded bytes was send => garbage.
    MEMORY_ERR_OUT_OF_BOUND_ACCESS = 7  # Trying to read more the maximum size of the section. Trying to write more than 32 KiB.
    MEMORY_ERR_NOT_IMPLEMENTED = 4
    MEMORY_ERR_FLASH = 20  # general QSPI flash write / read error.
    MEMORY_ERR_LENGTH_INVALID_ARGUMENT = 8  # Trying to write 0 bytes.
    MEMORY_ERR_MAX = 0xffff


class mfx4ARMadillo(mfx4Controller):
    """Class representing an MFX_4 ARMadillo.

    Using the ARMadillo CANOpen Object 0x2010 interface through the
    CMMemory module:
    Write / read / erase single pieces or all configuration maps of the armadillo.
    Write / read / erase i2c eeproms.
    Write / read / erase voucherdata.
    """

    def __init__(self, NodeId):
        self._Node = NodeId
        ds.storage.AddGenericDevice(NodeId)
        self.GetInfo()
        self.done = False
        self.package = 0
        self.packageTodo = 0
        self.cancel = 0
        self.ModuleLinkageMap = None
        self.ModuleAccessMap = None
        self.ModuleQuantityMap = None
        self.data = ""
        self.SystemLogMessages = []

    def TheNode(self):
        return self._Node

    MemoryInterfaceRX = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x08), NodeId=TheNode)
    MemoryInterfaceTX = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x07), NodeId=TheNode)
    MemoryInterfaceError = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x09), NodeId=TheNode)

    MemoryInterfaceLength = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x02), NodeId=TheNode)
    MemoryInterfaceAddress = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x03), NodeId=TheNode)
    MemoryInterfaceSection = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x05), NodeId=TheNode)
    MemoryInterfaceOperation = ds.dsproperty(Address=FullIndex(0, 0x2010, 0x0C), NodeId=TheNode)

    def MemoryInterfaceChange(self, FI, Value):
        isSuccess = False
        if FI == self.MemoryInterfaceError.FIndex:
            isSuccess = (memoryErrorEnum(int(Value)) == memoryErrorEnum.MEMORY_ERR_NONE_READ_SUCCESS
                         or memoryErrorEnum(int(Value)) == memoryErrorEnum.MEMORY_ERR_NONE_WRITE_TO_RAM_SUCCESS
                         or memoryErrorEnum(int(Value)) == memoryErrorEnum.MEMORY_ERR_NONE_WRITE_RAM_TO_SECTION_SUCCESS)

            if memoryErrorEnum(int(Value)) == memoryErrorEnum.MEMORY_ERR_NONE_WRITE_TO_RAM_SUCCESS:
                self.package += 1
                mfl.info(f"Package:{self.package}/{self.packageTodo}")
                self.done = True
                return

            elif memoryErrorEnum(int(Value)) == memoryErrorEnum.MEMORY_ERR_NONE_WRITE_RAM_TO_SECTION_SUCCESS:
                mfl.info("Written RAM to exFlash.")
                return

        if FI == self.MemoryInterfaceError.FIndex and not isSuccess:
            mfl.error(f"ERROR:: {Value} ({memoryErrorEnum(int(Value)).name})")
            self.cancel = int(Value)
            return

        if FI == self.MemoryInterfaceRX.FIndex:
            if not self.MemoryInterfaceRX.Value:
                print("Empty RX")
            self.package += 1
            
            mfl.info(f"Package:{self.package}/{self.packageTodo}")
            self.done = True
            self.data += self.MemoryInterfaceRX.Value
            return

        if FI == self.MemoryInterfaceTX.FIndex:
            return

    def SetMemoryNotifications(self):
        self.ResetInterfaceFields()
        time.sleep(0.2)

        ds.storage.SetNotification(self.MemoryInterfaceRX, 0, self.MemoryInterfaceChange, False)
        time.sleep(0.1)
        ds.storage.SetNotification(self.MemoryInterfaceTX, 0, self.MemoryInterfaceChange, False)
        time.sleep(0.1)
        ds.storage.SetNotification(self.MemoryInterfaceError, 0, self.MemoryInterfaceChange, False)
        time.sleep(0.2)

    def RemoveMemoryNotifications(self):
        time.sleep(0.2)
        ds.storage.RemoveNotification(self.MemoryInterfaceRX)
        time.sleep(0.1)
        ds.storage.RemoveNotification(self.MemoryInterfaceTX)
        time.sleep(0.1)
        ds.storage.RemoveNotification(self.MemoryInterfaceError)
        time.sleep(0.1)

        self.ResetInterfaceFields()
        time.sleep(0.2)

    def GetADCConfiguration(self):
        """Testing todo."""
        self.GetMemoryData(0, 512, memorySectionEnum.MEMORY_SECTION_CPU_I2C_EEPROM)
        time.sleep(0.6)
        hhh = binascii.unhexlify(self.data)
        return hhh

    def GetCommonHeader(self, address):
        """Sneak peak at the address as to gauge how much needs to be downloaded."""
        self.GetMemoryData(address, 30, memorySectionEnum.MEMORY_SECTION_CPU_QSPI_FLASH)
        time.sleep(0.6)
        CH = commonHeader_t()
        CH.Unpack(binascii.unhexlify(self.data))
        return CH

    def GetMap(self, configurationInstance, configurationLocation):
        mfl.setLevel(logging.INFO)
        totalBytes = self.GetCommonHeader(configurationLocation).ulTotalByteCount
        if totalBytes > 256:
            self.GetMemoryData(configurationLocation, totalBytes, memorySectionEnum.MEMORY_SECTION_CPU_QSPI_FLASH)
            time.sleep(0.6)
        a = self.CheckMemoryDataIsValid(self.data)
        if not a:
            return None
        # print(self.data)
        configurationInstance.Unpack(binascii.unhexlify(self.data))
        configurationInstance.Sort()
        mfl.setLevel(logging.WARNING)
        return configurationInstance

    def GetLinkageMap(self):
        mfl.warning("##############################")
        mfl.warning("###### Get Linkage Map  ######")
        self.ModuleLinkageMap = self.GetMap(moduleLinkageHeader_t(), CMemoryLocations.xFlashModuleLinkageLocation)
        return self.ModuleLinkageMap

    def GetAccessMap(self):
        mfl.warning("##############################")
        mfl.warning("######  Get Access Map  ######")
        self.ModuleAccessMap = self.GetMap(moduleAccessMapHeader_t(), CMemoryLocations.xFlashModuleAccessLocation)
        return self.ModuleAccessMap

    def GetLinkageMap_Counter_Product(self):
        mfl.warning("#########################################")
        mfl.warning("## Get Linkage Map Counter <=> Product ##")
        self.ModuleLinkageMap = self.GetMap(moduleLinkageHeader_t(), CMemoryLocations.xFlashCounterProductLinkageLocation)
        return self.ModuleLinkageMap

    def GetLinkageMap_Product_ProcessControl(self):
        mfl.warning("################################################")
        mfl.warning("## Get Linkage Map Product <=> ProcessControl ##")
        self.ModuleLinkageMap = self.GetMap(moduleLinkageHeader_t(), CMemoryLocations.xFlashProductProcessControlLinkageLocation)
        return self.ModuleLinkageMap

    def GetQuantityMap(self):
        mfl.warning("##############################")
        mfl.warning("###### Get Quantity Map ######")
        self.ModuleQuantityMap = self.GetMap(moduleQuantityHeader_t(), CMemoryLocations.xFlashModuleQuantityLocation)
        return self.ModuleQuantityMap

    def GetAllMaps(self):
        mfl.warning("########################################")
        mfl.warning("###### Get All Configuration Maps ######")
        return [self.GetQuantityMap(),
                self.GetLinkageMap(),
                self.GetLinkageMap_Counter_Product(),
                self.GetLinkageMap_Product_ProcessControl(),
                self.GetAccessMap()]

    def SetMap(self, map):
        """Write a configration structure to the correct space in ARMadillo memory."""

        mfl.setLevel(logging.INFO)
        def prvSetTheMap(map):
            mfl.warning("##############################")
            if isinstance(map, moduleAccessMapHeader_t):
                mfl.warning("###### Set Access Map ######")
                flashLocation = CMemoryLocations.xFlashModuleAccessLocation
            elif isinstance(map, moduleQuantityHeader_t):
                mfl.warning("###### Set Quantity Map ######")
                flashLocation = CMemoryLocations.xFlashModuleQuantityLocation
            elif isinstance(map, moduleLinkageHeader_t) and map.xCommonHeader.ucCopyId == 0:
                mfl.warning("###### Set Linkage Map ######")
                flashLocation = CMemoryLocations.xFlashModuleLinkageLocation
            elif isinstance(map, moduleLinkageHeader_t) and map.xCommonHeader.ucCopyId == 1:
                mfl.warning("# Set Linkage Map Counter <=> Product #")
                flashLocation = CMemoryLocations.xFlashCounterProductLinkageLocation
            elif isinstance(map, moduleLinkageHeader_t) and map.xCommonHeader.ucCopyId == 2:
                mfl.warning("# Set Linkage Map Product <=> ProcessControl #")
                flashLocation = CMemoryLocations.xFlashProductProcessControlLinkageLocation
            else:
                return False

            ret = False
            map.Prepare()
            mfl.warning(f"Checksum: {map.xCommonHeader.usOverallChecksum}")
            mfl.warning(f"Bytes: {map.xCommonHeader.ulTotalByteCount}")
            bin = map.Pack()
            self.WriteToRAM(0, len(bin), bin, memorySectionEnum.MEMORY_SECTION_CPU_QSPI_FLASH)
            time.sleep(1)
            a = memoryErrorEnum(int(self.MemoryInterfaceError.Value))
            if a == memoryErrorEnum.MEMORY_ERR_NONE_WRITE_TO_RAM_SUCCESS:
                self.WriteRAMtoSection(flashLocation, len(bin), memorySectionEnum.MEMORY_SECTION_CPU_QSPI_FLASH)
                time.sleep(1)
                a = memoryErrorEnum(int(self.MemoryInterfaceError.Value))
                ret = a == memoryErrorEnum.MEMORY_ERR_NONE_WRITE_RAM_TO_SECTION_SUCCESS

            if ret:
                mfl.warning("Successfully written map to Flash.")
            else:
                mfl.error("Failed writting map to Flash. Err: {a}")

            mfl.warning("Retrieve written header and checksum...")
            CH = self.GetCommonHeader(flashLocation)
            mfl.warning(f"Checksum Local: {map.xCommonHeader.usOverallChecksum}")
            mfl.warning(f"Checksum Remote: {CH.usOverallChecksum}")
            return CH.usOverallChecksum == map.xCommonHeader.usOverallChecksum

        ret = False
        if isinstance(map, collections.abc.Sequence):
            for theMap in map:
                ret = prvSetTheMap(theMap)
                if not ret:
                    return ret

        else:
            ret = prvSetTheMap(map)
        mfl.setLevel(logging.WARNING)
        return ret

    def ResetInterfaceFields(self):
        ds.storage.Set(self.MemoryInterfaceSection, 0)
        time.sleep(0.1)
        ds.storage.Set(self.MemoryInterfaceError, memoryErrorEnum.MEMORY_ERR_NONE)
        time.sleep(0.1)
        ds.storage.Set(self.MemoryInterfaceLength, 0)
        time.sleep(0.1)
        ds.storage.Set(self.MemoryInterfaceAddress, 0)
        time.sleep(0.1)
        ds.storage.Set(self.MemoryInterfaceOperation, 0)
        time.sleep(0.1)

    def GetMemoryData(self, address, length, section):
        """Get <length> amount of data at address <address> from section <section>.

        [todo] uses while loop.
        """
        self.SetMemoryNotifications()
        ds.storage.Set(self.MemoryInterfaceSection, section.value)

        self.package = 0
        self.done = False
        self.data = ""
        self.packageTodo = length / 256
        p = 0
        if self.packageTodo - int(self.packageTodo) > 0:
            p = 1
        self.packageTodo = int(self.packageTodo) + p

        while self.cancel == 0 and length > 0:
            self.done = False
            ds.storage.Set(self.MemoryInterfaceLength, 256)
            ds.storage.Set(self.MemoryInterfaceAddress, address)
            ds.storage.Set(self.MemoryInterfaceOperation, memoryOperationEnum.MEMORY_OPERATION_READ)
            length -= 256
            address += 256
            while not self.done:
                if self.cancel != 0:
                    break
                time.sleep(0.3)
                pass

        self.RemoveMemoryNotifications()

        self.package = 0
        self.done = False
        self.packageTodo = 0

        if self.cancel != 0:
            self.RaiseMemoryErrorException()
        self.cancel = 0

    def RaiseMemoryErrorException(self):
        mfl.error(f'Error {self.cancel} occured when trying to download memory.')
        raise Exception(f"MemoryError: {self.cancel} {memoryErrorEnum(int(self.cancel)).name}")

    def WriteToRAM(self, address, length, data, section):
        """Write <length> amount of data from address <address> into the 32 KiB RAM in max of 256 bytes.

        [todo] uses while loop.
        """
        if len(data) < length:
            return False

        self.RemoveMemoryNotifications()
        self.SetMemoryNotifications()

        ds.storage.Set(self.MemoryInterfaceSection, section.value)
        time.sleep(0.5)

        self.package = 0
        self.done = False
        self.data = ""
        self.packageTodo = length / 256
        p = 0
        if self.packageTodo - int(self.packageTodo) > 0:
            p = 1
        self.packageTodo = int(self.packageTodo) + p

        retry = 0

        while self.cancel == 0 and length > 0:
            waitfor = 0
            def localFun():
                self.done = False
                p = 256
                if length < 256:
                    p = (length % 256)
                ds.storage.Set(self.MemoryInterfaceLength, p)
                time.sleep(0.1)
                ds.storage.Set(self.MemoryInterfaceAddress, address)
                time.sleep(0.1)
                dat = data[address:address + p].hex()
                # ds.storage.SetBinary(self.MemoryInterfaceTX, dat)
                ds.storage.Set(self.MemoryInterfaceTX, dat)
                mfl.info(f"P{self.package}: {dat}")
                time.sleep(0.5)
                ds.storage.Set(self.MemoryInterfaceOperation, int(memoryOperationEnum.MEMORY_OPERATION_WRITE_RAM))
                time.sleep(0.5)
                return p
            
            while retry < 4:
                waitfor = 0
                p = localFun()

                if self.done:
                    break

                while not self.done and waitfor < 5:
                    time.sleep(0.3)
                    if self.cancel != 0:
                        break
                    waitfor = waitfor + 1
                    pass
                if not self.done:
                    retry = retry + 1
                    mfl.error(f"P{self.package}: retry:{retry}")
                
                if self.cancel == memoryErrorEnum.MEMORY_ERR_ACCESS_DENIED.value:
                    raise mfx4ExceptionElevationNeeded("ARMadillo elevation needed. No access rights.")

                if retry > 5:
                    raise mfx4ExceptionSystemIsNotResponsive("5 retries failed. System is not responding.")

            length -= p
            address += p

        time.sleep(0.5)
        self.RemoveMemoryNotifications()

        self.package = 0
        self.done = False
        self.packageTodo = 0

        if self.cancel != 0:
            self.RaiseMemoryErrorException()

        self.cancel = 0

    def WriteRAMtoSection(self, address, length, section):
        """Commit/Write <length> amount of data from the RAM to the section <section> at address <address>."""
        if length > CMemoryLocations.xConfigurationRAMBufferSize:
            return

        self.SetMemoryNotifications()

        ds.storage.Set(self.MemoryInterfaceSection, section.value)
        ds.storage.Set(self.MemoryInterfaceError, 0)
        ds.storage.Set(self.MemoryInterfaceLength, length)
        ds.storage.Set(self.MemoryInterfaceAddress, address)
        time.sleep(0.2)
        ds.storage.Set(self.MemoryInterfaceOperation, int(memoryOperationEnum.MEMORY_OPERATION_WRITE_RAM_TO_SECTION))

        self.RemoveMemoryNotifications()

    def Erase(self, address, length, section):
        self.SetMemoryNotifications()

        ds.storage.Set(self.MemoryInterfaceSection, section.value)
        ds.storage.Set(self.MemoryInterfaceError, 0)
        ds.storage.Set(self.MemoryInterfaceLength, length)
        ds.storage.Set(self.MemoryInterfaceAddress, address)
        time.sleep(0.2)
        ds.storage.Set(self.MemoryInterfaceOperation, int(memoryOperationEnum.MEMORY_OPERATION_ERASE))

        self.RemoveMemoryNotifications()

    def EraseVouchers(self):
        self.Erase(CMemoryLocations.xFlashVoucherLocation,
                   CMemoryLocations.xFlashVoucherSize,
                   memorySectionEnum.MEMORY_SECTION_CPU_QSPI_FLASH)

    def CheckMemoryDataIsValid(self, data):
        """Only check the commonHeader CRC of a given data array."""
        hexdat = binascii.unhexlify(data)
        CH = commonHeader_t()
        CH.Unpack(hexdat)
        c = commonHeader_t.crc_calc(0, hexdat)
        return c == CH.usOverallChecksum

    def GetSystemLog(self):
        self.GetMemoryData(CMemoryLocations.xFlashSystemLogsLocation,
                           CMemoryLocations.xFlashSystemLogsSize,
                           memorySectionEnum.MEMORY_SECTION_CPU_QSPI_FLASH)
        e = binascii.unhexlify(self.data)
        self.SystemLogMessages = []
        while len(e) > 0:
            lgMsg = mfAE.logMessage_t()
            lgMsg.Unpack(e)
            self.SystemLogMessages.append(lgMsg)
            e = e[64:]
        return self.SystemLogMessages

    def Get_CPU_I2C_EEPROM_Data(self):
        self.GetMemoryData(0, 64 * 1024,
                           memorySectionEnum.MEMORY_SECTION_CPU_I2C_EEPROM)
        return binascii.unhexlify(self.data)

    def Get_AIO_I2C_EEPROM_Data(self):
        self.GetMemoryData(0, 8 * 1024,
                           memorySectionEnum.MEMORY_SECTION_AIO_I2C_EEPROM)
        return binascii.unhexlify(self.data)

    def Get_AIO_ConfigurationData(self):
        self.GetMemoryData(0, 194,
                           memorySectionEnum.MEMORY_SECTION_AIO_I2C_EEPROM)
        print(self.data)
        return binascii.unhexlify(self.data)
