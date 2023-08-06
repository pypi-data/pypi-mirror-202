import datetime
import logging
import socket
import struct
import time

from src import iupy

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("iupy/test_sap")

    myip = iupy.get_my_ip("172.30.0.141")

    datetime_int = int(datetime.datetime.utcnow().timestamp())

    session_info = "v=0\r\n" \
                   "o=- {} {} IN IP4 172.30.0.141\r\n" \
                   "s=4.1: WBZ-DT\r\n" \
                   "i=DVBlast Video Network\r\n" \
                   "c=IN IP4 239.255.1.1/255\r\n" \
                   "t=0 0\r\n" \
                   "a=recvonly\r\n" \
                   "a=type:broadcast\r\n" \
                   "a=source-filter: incl IN IP4 * 172.30.0.141\r\n" \
                   "m=video 28001 udp mpeg\r\n".format(datetime_int, datetime_int)

    sap_struct = iupy.sap_segment(version=1, src_ip_addr=myip, id_hash=2,
                                  payload_type='application/sdp', payload=session_info)

    if sap_struct is None:
        print("Unable to build SAP Packet.  Check debug Logs.")
        exit()

    print("SAP Structure: ", ' '.join(hex(byte)[2:].zfill(2) for byte in sap_struct))

    beaconSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    beaconSocket.settimeout(0.2)
    beaconSocket.setsockopt(socket.IPPROTO_IP, socket.SO_REUSEADDR, 1)
    # beaconSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(myip))
    beaconSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('B', 16))

    beaconDest = ('224.2.127.254', 9875)

    done = False
    i = 0
    while not done:
        beaconSocket.sendto(sap_struct, beaconDest)

        time.sleep(5)

        i += 1;
        if i > 6:
            done = True

    beaconSocket.close()

    print("SAP Complete")
