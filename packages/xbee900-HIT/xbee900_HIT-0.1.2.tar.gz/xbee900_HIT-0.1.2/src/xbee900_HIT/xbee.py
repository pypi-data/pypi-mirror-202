import signal
import time
import logging
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress
from . import packet

# Timeout exception and handler


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException('Function timed out')


class Data:
    """
    Data class used to store packets in receiver buffer

Attributes:
    time: time when the data is created
    data: dict of packets
    expired: time when the data is expired
    """

    def __init__(self, expired=30):
        """
        Constructor of Data class
        :param expired: time when the data is expired, default is 30s
        """
        self.time = time.time()
        self.data = {}
        self.expired = expired

    def is_expired(self) -> bool:
        """
        Check if the data is expired
        :return: True if expired, False otherwise
        """
        return time.time() - self.time > self.expired

    def append(self, p) -> None:
        """
        Append a packet to the data
        :param p: packet to data
        :return: None
        """
        self.data[p.seq] = p

    def get_data(self) -> bytes:
        """
        Get data from the data
        :return: raw data of packets
        """
        sorted_data = sorted(self.data.items())
        packets = []
        for _, value in sorted_data:
            packets.append(value)
        return packet.get_data(packets)

    def __len__(self):
        return len(self.data)


class Xbee:
    """
    Xbee class used to send and receive data

Attributes:
    __no: packet number,[0,255]
    __port: port of xbee device
    __baud_rate: baud rate of xbee device
    __device: xbee device class
    __dev: str of xbee device 64bits address
    """

    def __init__(self, port, baud_rate):
        """
        Constructor of Xbee class
        :param port: port of xbee device
        :param baud_rate: baud rate of xbee device
        """
        self.__no = 0
        self.__port = port
        self.__baud_rate = baud_rate
        self.__device = XBeeDevice(port, baud_rate)
        self.__dev = 1
        try:
            self.__device.open()
            self.__dev = self.__device.get_64bit_addr()
        except Exception as e:
            logging.error(f"Xbee device open error: {e}")
        logging.debug(
            f"Xbee device opened, port: {port}, baud_rate: {baud_rate}")

    def send_data_broadcast(self, data) -> bool:
        try:
            self.__device.send_data_broadcast(data)
        except Exception as e:
            logging.warning(f"{self.__dev}:Xbee send data error: {e}")
            return False
        logging.debug(f"{self.__dev}:Xbee send data: {data} ")
        return True

    def add_receive_data_callback(self, callback=None):
        if callback is not None:
            self.__device.add_data_received_callback(callback)

    def send_data(self, data, remote):
        try:
            self.__device.send_data(remote, data)
        except Exception as e:
            logging.warning(
                f"{self.__dev}:Xbee send data to {remote} error: {e}")

    def receive_data(self) -> (bytes, RemoteXBeeDevice):
        try:
            xbee_message = self.__device.read_data()
            if xbee_message is not None:
                data = xbee_message.data
                remoteAddr = xbee_message.remote_device.get_64bit_addr()
                logging.debug(f"{self.__dev}:Xbee receive data: {data} ")
                return data, remoteAddr

            else:
                return b"", None
        except Exception as e:
            logging.warning(f"{self.__dev}:Xbee receive data error: {e}")
            return b"", None

    def send_packet(self, data: bytes, payload=256, wait=0, remoteAddr=None) -> bool:
        """
        Send data to remote device
        :param data: data bytes need to be sent
        :param payload: max payload of each packet
        :param wait: time to wait between each packet, 0 is no wait
        :param remoteAddr: If none, use broadcast, otherwise use remoteAddr
        :return: True if success
        """
        remote = None
        if remoteAddr is not None:
            remote = self.get_remote_device(remoteAddr)
        self.__no = (self.__no + 1) % 256
        data_with_seq = packet.get_packets(self.__no, data, payload)
        try:
            for data in data_with_seq:
                if remote is not None:
                    self.send_data(data.encode(), remote)
                elif self.send_data_broadcast(data.encode()) is False:
                    logging.warning(f"{self.__dev}:Xbee send packet failed")
                    return False
                time.sleep(wait)
        except Exception as e:
            logging.warning(f"{self.__dev}:Xbee send packet error: {e}")
            return False
        logging.debug(
            f"{self.__dev}:Xbee send {len(data_with_seq)} packets, payload: {payload}")
        return True

    def receive_packet(self, timeout=0) -> (bytes, RemoteXBeeDevice):
        """
        Receive data from remote device
        :param timeout: Time to wait between each packet, 0 is no wait
        :return: data bytes received and remote device address
        """
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        received_data = {}
        try:
            while True:
                data_with_seq, remoteAddr = self.receive_data()
                if data_with_seq is None or len(data_with_seq) == 0:
                    continue
                p = packet.Packet.decode(data_with_seq)
                index = f"{remoteAddr}:{p.no}"
                if received_data.get(index) is None or received_data.get(index).is_expired():
                    received_data[index] = Data()
                received_data[index].append(p)
                logging.debug(f"{self.__dev}:Xbee receive packet: {p} ")
                if len(received_data[index]) == p.total:
                    break
        except TimeoutException as ex:
            logging.warning(ex)
        finally:
            signal.alarm(0)
            original_message = received_data[index].get_data()
            logging.debug(
                f"{self.__dev}:Xbee receive {len(received_data[index])} packets")
            del received_data[index]
            return original_message, remoteAddr

    def get_remote_device(self, remote_address: str) -> RemoteXBeeDevice:
        return RemoteXBeeDevice(self.__device, XBee64BitAddress.from_hex_string(remote_address))

    def close(self):
        self.__device.close()

    def __del__(self):
        self.close()
