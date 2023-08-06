import ipaddress
import logging
import re
import socket
import struct

# Default module logger

logger = logging.getLogger("iupy/network")


# Host Utilities

def get_my_ip(destination=None):
    """
    This function returns a string which contains the host's source IP address for connections to a given destination.
    In the absensce of a destination, well-know address of 4.2.2.1 will be used to make the determination.

    The function uses the dual-stack AF_INET6 family by default.  A value of None will be returned if a valid IP
    address cannot be determined.

    The only allowable optional keyword is version, which should be either 4 or 6, which have the following effects:

    * Specifying version 4 will use the AF_INET socket only, returning IPv4 addresses only.
    * Specifying version 6 will use return any IPv4 address as IPv6 masked format.

    :param destination:
    :param kwargs:
    :return:
    """

    _logger = logging.getLogger("iupy/network/get_my_ip")

    # Specify the destination as well-known 4.2.2.1 if no value is specified:
    if destination:
        test_ip = socket.gethostbyname(destination)
    else:
        test_ip = socket.gethostbyname("4.2.2.1")

    # Use of dual-stack for IPv4 addresses barfs in Python 3.8 open the socket based on the specific test IP.
    if ipaddress.ip_address(test_ip).version == 4:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    # Open our socket to the specified destination.
    try:
        s.connect((test_ip, 1))
        my_ip = ipaddress.ip_address(s.getsockname()[0])
    except socket.error as error_message:
        _logger.debug("Socket error for {} / {}".format(test_ip, error_message))
        my_ip = None
    finally:
        s.close()

    # Return None from the previous socket error.
    if not my_ip:
        return None

    # If this is IPv6, check and see if we have a mapped IPv4 object.
    # Convert this to an IPv4 address if version 6 was not explicitly specified.

    if my_ip.version == 6 and my_ip.ipv4_mapped:
        my_ip = ipaddress.IPv4Address(int(ipaddress.ip_address(str(my_ip).replace('::ffff:', '::'))))

    _logger.debug("Source address to reach {} is {}.".format(test_ip, my_ip))

    return str(my_ip)


# ACL Utilities

def v4_bits_to_mask(v4_bitlength):
    """
    Returns an IPv4 Netmask based upon a number of bits from 0-32.

    Returns None if the mask source is not in range or is otherwise invalid.

    :param v4_bitlength:
    :return:
    """

    logger = logging.getLogger("iupy/network/v4_bits_to_mask")

    # Return the netamsk, value if the format is valid.

    try:
        netmask = str(ipaddress.IPv4Network(("0.0.0.0/{}").format(v4_bitlength)).netmask)
        logger.debug("Netmask for {} is {}".format(v4_bitlength, netmask))

    except ipaddress.NetmaskValueError as error_message:
        netmask = None
        logger.debug("{}".format(error_message))

    return netmask


def v4_mask_to_bits(v4_mask):
    """
    This function takes in a netmask and returns the proper consecutive bitwise value.

    This only counts the bits from left to right until the first 0 is reached.  For example, a submitted mask
    of 255.255.0.255 will return a bit value of 16, and not 24.

    The function returns None if the mask does not meet the IPv4 Regex.

    :param v4_mask:
    :return:
    """

    logger = logging.getLogger("iupy/network/v4_mask_to_bits")

    # Get the bits out of a valid netmask, else return None.

    try:
        bit_value = ipaddress.IPv4Network(("0.0.0.0/{}").format(v4_mask)).prefixlen
        logger.debug("Bits in {} is {}".format(v4_mask, bit_value))

    except ipaddress.NetmaskValueError as error_message:
        bit_value = None
        logger.debug("{}".format(error_message))

    return bit_value


def v4_wildcard(v4_mask):
    """
    This function returns a wildcard mask based upon either a valid bit length or IP Address.  This is different than
    a hostmask provided by the ipaddress library, because wildcard mask does not need to have consecutive bits.

    A bit length will be converted into a netmask first.

    :param v4_mask:
    :return:
    """

    logger = logging.getLogger("iupy/network/v4_wildcard")

    bitbox = ''

    # If we have a numeric between 0-32, get the netmask value.

    if re.search(r'^([0-9]|[12][0-9]|3[0-2])$', str(v4_mask)):
        v4_mask = v4_bits_to_mask(v4_mask)

    # Verify the netmask meets a strict IPv4 format.

    if re.search(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                 str(v4_mask)):

        # Convert the integer value of the address into bits, stripping out the "0b" binary indicator.

        bitbox = str(bin(int(ipaddress.ip_address(v4_mask)))).replace('0b', '')

        # Fill the full value out to 32 bits, if necessary.
        filler = ''

        for i in range(len(bitbox), 32):
            filler += "0"

        bitbox = filler + bitbox

    # If the bitbox is empty, then we did not have a valid source.  Return None.

    if bitbox == '':
        logger.debug("Invalid wildcard source: {}".format(v4_mask))
        return None

    # Invert all the bits.

    bitflip = ''

    for c in bitbox:
        if c == "1":
            bitflip += "0"
        else:
            bitflip += "1"

    wildcard_mask = str(ipaddress.ip_address(int(bitflip, 2)))

    # Uncomment below to send the bit values to debug
    # logger.debug("Bitbox {} / Bitflip {}".format(bitbox, bitflip))

    logger.debug("Wildcard for {} is {}".format(v4_mask, wildcard_mask))

    return wildcard_mask


def aclv4_hostmask(host_mask):
    """
    Returns a Cisco friendly text for a given host and netmask.

    :param host_mask:
    :return:
    """
    logger = logging.getLogger("iupy/network/v4_wildcard")

    logger.debug("Input: {}".format(host_mask))

    ip_info = host_mask.split("/")

    # Host Exceptions
    try:
        # Check /32 host exception
        if int(ip_info[1]) == 32:
            output = "host {}".format(ip_info[0])
            return output
    except IndexError:
        # Host if no mask was provided
        output = "host {}".format(ip_info[0])
        return output

    # Get the wildcard mask
    wildcard = v4_wildcard(ip_info[1])

    # Return the valid host wildcard value, otherwise return None.
    if wildcard is not None:
        return "{} {}".format(ip_info[0], wildcard)
    else:
        return None


def routev4_hostmask(host_mask):
    """
    Returns a Cisco friendly text for a given host and netmask.

    :param host_mask:
    :return:
    """
    _logger = logging.getLogger("iupy/network/routev4")

    _logger.debug("Input: {}".format(host_mask))

    ip_info = host_mask.split("/")

    # Host Exceptions
    try:
        # Check /32 host exception
        if int(ip_info[1]) == 32:
            mask = v4_bits_to_mask(32)
            return "{} {}".format(ip_info[0], mask)
    except IndexError:
        # Host if no mask was provided
        mask = v4_bits_to_mask(32)
        return "{} {}".format(ip_info[0], mask)

    # Get the wildcard mask
    mask = v4_wildcard(ip_info[1])

    # Return the valid host wildcard value, otherwise return None.
    if mask is not None:
        return "{} {}".format(ip_info[0], mask)
    else:
        return None


def sap_segment(*, version=1, src_ip_addr=None, reserved=False, announce=True, encrypted=False, compressed=False,
                auth_data=None, id_hash=None, payload_type=None, payload=None):
    """
    This function returns a SAP segment based on RFC-2974.

    The segment generated strictly matches the format of the packet only.  it is possible to generate a
    segment that is not RFC-compliant.  For example, generating a SAP announcement with version 6, which
    is not a valid value.

    https://www.rfc-editor.org/rfc/rfc2974
    """

    _logger = logging.getLogger("iupy/network/sap_segment")

    # Segment Header - SAP Version
    if type(version) is not int:
        _logger.debug("SAP Version {} must be an integer value.".format(version))
        return None
    if version < 0 or version > 7:
        _logger.debug("SAP Version {} is not between 0 and 7.".format(version))
        return None
    hdr_v = format(version, '0>3b')   # Version

    # Segment Header - Address Type
    try:
        ip_addr_object = ipaddress.ip_address(src_ip_addr)
    except ValueError:
        _logger.debug("{} is not a valid IP address.".format(src_ip_addr))
        return None
    if ip_addr_object.version == 6:
        hdr_a = 1
    else:
        hdr_a = 0

    # Segment Header - Reserved Bit
    if reserved is True:
        hdr_r = 1
    else:
        hdr_r = 0

    # Segment Header - Message Type
    if announce is True:
        hdr_t = 0
    else:
        hdr_t = 1

    # Segment Header - Encryption
    if encrypted is True:
        hdr_e = 1
    else:
        hdr_e = 0

    # Segment Header - Compression
    if compressed is True:
        hdr_c = 1
    else:
        hdr_c = 0

    # Segment Header - First Byte
    hdr_bits = "{}{}{}{}{}{}".format(hdr_v, hdr_a, hdr_r, hdr_t, hdr_e, hdr_c)
    hdr_byte = struct.pack('b', int(hdr_bits, 2))

    # Authentication length as a number of 4-byte words.
    if auth_data is not None:
        if len(auth_data) % 4 != 0:
            _logger.debug("Authentication data length must be a multiple of 4.")
            return None
        hdr_auth_length = struct.pack('b', (len(auth_data) // 4))
    else:
        hdr_auth_length = struct.pack('b', 0)

    # Message ID Hash
    if (id_hash is None) or (type(id_hash) is not int):
        _logger.debug("ID Hash must be an integer between 0 and 65535")
        _logger.debug("{}, type {}".format(id_hash, type(id_hash)))
        return None
    if id_hash < 0 or id_hash > 65535:
        _logger.debug("ID hash is out of range.")
        return None
    hdr_id_hash = struct.pack('H', id_hash)

    # Originating Source IP Address
    hdr_src_addr = ip_addr_object.packed

    # Start building the segment.
    segment = hdr_byte + hdr_auth_length + hdr_id_hash + hdr_src_addr

    # Optional - Authentication Data
    if auth_data is None:
        _logger.debug("No authentication data provided.")
    elif type(auth_data) is not bytes:
        _logger.debug("Authentication data must be of bytes type.  Skipping.")
    else:
        segment += auth_data

    # Optional - Payload Type
    if len(payload_type) == 0:
        _logger.debug("No payload type provided.")
    else:
        segment += bytes(payload_type, 'utf-8')
        segment += b'\x00'

    # Payload
    if payload is None:
        _logger.debug("Payload cannot be empty.")
        return None
    else:
        segment += bytes(payload, 'utf-8')

    return segment
