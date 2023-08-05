"""Provides convenient functions to connect to MFX_4 devices.

This file contains the following functions:
    * mfx_endpoints - creates the connection, returns a tuple of MFX_4 device Endpoints.
    * mfx_close_endpoints - closes the connection
"""

import pymfx4.mfdatastorage as ds
from pymfx4.mffullindex import FullIndex
from pymfx4 import mfl

import socket
import serial
import time
import threading
import re
import sys
import traceback



class mfx4ExceptionEndpointDirect(Exception):
    pass


class mfx4ExceptionEndpointRemote(Exception):
    pass


class mfconnection:
    """Creates a connection to an MFX_4 device.

    Creates a connection (primarily socket TCP-IP) with an MFX_4 device and
    starts a read-thread to interpret the incoming MFX_4 protocol messages.
    Appropriately wraps (MFX_4 protocol) and writes bytes/strings into the socket.
    This class is not used directly, see mfx_endpoints and mfx_close_endpoints.
    """

    TCPIP_STR = "TCPIP"
    SERIAL_STR = "SERIAL"
    DUMMY_STR = "DUMMY"

    def __init__(self, config, tim=5):
        self.config = config
        self.TheEncoding = "ascii"
        self.sock = None
        self.connectionType = None
        self.CloseThreads = False
        self.timeouts = 0
        self.timeout = tim
        self.dataBuf = bytearray()
        self.SocketException = False

    @property
    def IsDummy(self):
        return self.connectionType == mfconnection.DUMMY_STR

    def _read_from_port(self):
        start = time.time()
        while True:
            if self.CloseThreads:
                return
            try:
                data = self.Read(512)
                self.dataBuf.extend(data)
                # print("Data rcvd: ", len(data))
                # print(f"HOST <-{data}")
                if len(self.dataBuf) > 0 and b'\x60' in self.dataBuf:

                    mfl.debug(f"HOST <-Log_Encoded: {data.decode(self.TheEncoding, 'ignore')}")
                    mfl.debug(f"HOST <-Log_Raw: {data}")

                    messageStream = self.dataBuf.decode(self.TheEncoding, "ignore")
                    messages = messageStream.split("`")

                    self.dataBuf = bytearray()
                    if not messageStream.endswith("`"):
                        self.dataBuf.extend(messages[-1])
                        messages.remove(messages[-1])

                    for line in messages:
                        # print(line)
                        matchObj = re.match(r'(?P<cmd>.*?)_(?P<nodeid>.*?)_(?P<index>.*?)_(?P<subindex>.*?)_(?P<content>.*)', line, re.I | re.DOTALL)
                        if matchObj:
                            try:
                                fi = FullIndex(int(matchObj.group("nodeid")), int(matchObj.group("index")), int(matchObj.group("subindex")))
                                # print(fi)
                                # print(matchObj.group("content"))
                                content = matchObj.group("content")
                                ds.storage.Notify(fi, content)
                            except Exception as e:
                                try:
                                    mfl.critical(f"Exception: {e}")
                                    mfl.critical(f"Exception Occured; {traceback.format_exception(*sys.exc_info())}")
                                except Exception as ex2:
                                    raise Exception('Thread unknown exception occured.')
                theTime = time.time() - start
                if theTime > self.timeout:
                    if self.connectionType == mfconnection.TCPIP_STR:
                        self.SendBytes(bytes("`", self.TheEncoding, errors='strict'))
                    start = time.time()
            except Exception as ex:
                if self.connectionType == mfconnection.TCPIP_STR:
                    self.SendBytes(bytes("`", self.TheEncoding, errors='strict'))
                self.SocketException = True

    def Send(self, befehl):
        bf = bytes(befehl, self.TheEncoding, errors='strict')
        mfl.debug(f"HOST-> {befehl}")

        if self.connectionType == mfconnection.SERIAL_STR:
            self.sock.write(bf)
        elif self.connectionType == mfconnection.TCPIP_STR:
            try:
                self.sock.send(bf)
                self.timeouts = 0
            except socket.timeout:
                mfl.info("Send timed out.")
                self.timeouts = self.timeouts + 1
            except Exception as E:
                self.SocketException = True

    def SendBytes(self, theBytes):
        if self.connectionType == mfconnection.SERIAL_STR:
            self.sock.write(theBytes)
        elif self.connectionType == mfconnection.TCPIP_STR:
            try:
                self.sock.send(theBytes)
                self.timeouts = 0
            except socket.timeout:
                mfl.info("Send timed out.")
                self.timeouts += 1
            except Exception as E:
                self.SocketException = True

    def Read(self, bytes):
        rec = ""
        if self.connectionType == mfconnection.SERIAL_STR:
            rec = self.sock.read(bytes)
        elif self.connectionType == mfconnection.TCPIP_STR:
            rec = self.sock.recv(bytes,)
        return rec

    def close(self):
        try:
            if self.IsDummy:
                pass
            else:
                self.sock.close()
        except Exception as ex:
            pass

    def start_thread(self):
        if self.IsDummy:
            pass
        self.CloseThreads = False
        threading.Thread(target=self._read_from_port, name="ReadThread").start()
        # time.sleep(1)

    def close_thread(self):
        if self.IsDummy:
            pass
        self.CloseThreads = True
        time.sleep(5)

    def open(self):
        if "dummy" in self.config.lower():
            self.connectionType = mfconnection.DUMMY_STR
        elif "com" in self.config.lower():
            self.connectionType = mfconnection.SERIAL_STR
            address, baudrate, DATASIZE, PAR2, STOP = self.config.split(":")

            PAR = serial.PARITY_NONE
            if PAR2 == "E":
                PAR = serial.PARITY_EVEN
            elif PAR2 == "O":
                PAR = serial.PARITY_ODD

            self.sock = serial.Serial(address.lower(), int(baudrate), timeout=self.timeout, parity=PAR, bytesize=int(DATASIZE), stopbits=int(STOP))
        else:
            address, port = self.config.split(":")
            if not port:
                port = "4003"
            socket.setdefaulttimeout(None)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((address, int(port)))
            self.sock.send(bytes("`", self.TheEncoding, errors='strict'))
            self.connectionType = mfconnection.TCPIP_STR

    def open_and_start_thread(self):
        try:
            self.open()
            # time.sleep(0.1)
            self.start_thread()
            self.SocketException = False
            return True
        except Exception as Ex:
            mfl.critical(traceback.format_exc())
            pass
        return False

    def close_and_end_thread(self):
        try:
            self.close_thread()
            self.close()
            return True
        except Exception as ex:
            pass
        return False


def mfx_endpoints(mfx_connDevice, mfx_EndpointNodes):
    """Creates a connection with MFX_4 devices.

    Creates either a socket tcp/ip or serial connection with <mfx_connDevice>.
    Creates a read-thread to interpret the incoming MFX_4 protocol messages.
    Determines whether the listed <mfx_EndpointNodes> are online and adds them
    to the datastorage.

    TODO make more than one connection possible with this scheme.

    Args:
        mfx_connDevice (str): Create a connection to this device. E.g. 192.168.3.11:4004 or 9600:8:N:1
        mfx_EndpointNodes (list): List of node-ids that are to be expected.

    Returns:
        tuple: a tuple of objects in their relevant class. E.g. a mfx4Controller-instance
            is returned for each controller listed in <mfx_EndpointNodes>.

    Raises:
        mfx4ExceptionEndpointDirect: If no MFX_4 device can be determined through <mfx_connDevice>.
        mfx4ExceptionEndpointRemote: At least one listed endpoint in <mfx_EndpointNodes> can not be found.
    """

    from pymfx4.mfconnection import mfconnection
    import pymfx4.mfdatastorage as ds
    from pymfx4.mfx4ARMadillo import mfx4ARMadillo
    from pymfx4.mfx4device import mfx4device
    from pymfx4.mfx4device import mfx4Controller
    from pymfx4.mfx4device import mfx4Terminal
    from pymfx4.mfx4device import mfx4Cut
    from pymfx4 import mfl
    import time

    def DetermineDeviceTypeBy(Node):
        device = mfx4device(Node)
        time.sleep(0.5)
        for i in range(4):
            if device.SoftwareVersion.Value is not None:
                break
            device.GetInfo()
            time.sleep(0.5)

        firmware = ""
        if device.SoftwareVersion.Value is not None:
            firmware = device.SoftwareVersion.Value.lower()
        if firmware.find('ctl') >= 0:
            version = device.Version
            if version is not None:
                if version[0] > 2:
                    mfl.info("Node '{Node}' is mfx4ARMadillo.")
                    device = mfx4ARMadillo(Node)
                else:
                    mfl.info(f"Node '{Node}' is mfx4Controller.")
                    device = mfx4Controller(Node)
                time.sleep(0.5)
                for i in range(4):
                    if device.SoftwareVersion.Value is not None:
                        break
                    device.GetInfo()
                    time.sleep(0.5)

        elif firmware.find('term') >= 0 or firmware.find('cut') >= 0 or firmware.find('edi') >= 0:
            if firmware.find('term') >= 0:
                mfl.info(f"Node '{Node}' is mfx4Terminal.")
                device = mfx4Terminal(Node)
            else:
                mfl.info(f"Node '{Node}' is mfx4CUT.")
                device = mfx4Cut(Node)
            time.sleep(0.5)
            for i in range(4):
                if device.SoftwareVersion.Value is not None:
                    break
                device.GetInfo()
                time.sleep(0.5)

        return device

    # CONNECTION
    mfc = mfconnection(mfx_connDevice)
    ds.storage.mfc = mfc
    mfc.open_and_start_thread()

    # Fill Datastorage with correct eds/xdd
    devices = []

    ConnDevice = DetermineDeviceTypeBy(0)
    # time.sleep(1)
    if ds.storage.AddDevice(ConnDevice) is False:
        mfc.close_and_end_thread()
        mfl.error("Could not determine device-type (direct)")
        raise mfx4ExceptionEndpointDirect("Could not determine device-type (direct)")

    devices.append(ConnDevice)

    # Endpoint = ConnDevice

    N = mfx_EndpointNodes
    if not isinstance(N, list):
        N = [N]

    for node in N:
        if isinstance(node, str):
            node = int(node)
        if node > 0:
            Endpoint = DetermineDeviceTypeBy(node)
            if ds.storage.AddDevice(Endpoint) is False:
                mfc.close_and_end_thread()
                mfl.error("Could not determine device-type (remote)")
                raise mfx4ExceptionEndpointRemote("Could not determine device-type (remote)")

            devices.append(Endpoint)

    return tuple(devices)


def mfx_close_endpoints():
    """Closes the connection opened via mfx_endpoints.

    TODO make more than one connection possible with this scheme.
    """
    import pymfx4.mfdatastorage as ds
    if ds.storage.mfc:
        ds.storage.mfc.close_and_end_thread()
