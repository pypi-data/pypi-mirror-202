import logging
from src import iupy

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("iupy/test_network")

    # Default Value Tests

    assert iupy.get_my_ip() is not None, "IP should not return None.  The value can vary, however."

    # Loopback Tests

    assert iupy.get_my_ip("::1", version=4) is None, "IPv6 Loopback should be None in IPv4 Requests"
    assert iupy.get_my_ip("::1") == "::1", "IPv6 Loopback should return its address."

    assert iupy.get_my_ip('127.0.0.1') == '127.0.0.1', "Loopback should be returned as sent."
    assert iupy.get_my_ip('127.0.0.1', version=6) == '::ffff:7f00:1', "Loopback should be returned as sent."

    # DNS Host Tests

    assert iupy.get_my_ip('goob.goob') is None, "Bad name should not return an address."
    assert iupy.get_my_ip('google.com') is not None, "A valid DNS name should return a socket source."

    # Netmask to bit notation

    assert iupy.v4_mask_to_bits('255.255.255.0') == 24, "255.255.255.0 should be 24 bits."
    assert iupy.v4_mask_to_bits('255.255.0.255') is None, "255.255.0.255 should be an invalid mask."
    assert iupy.v4_mask_to_bits('0.255.255.255') == 8, "0.255.255.255 returns 8 bits as a wildcard."
    assert iupy.v4_mask_to_bits('255.255.255.255.255') is None, "Invalid mask should return None."

    # Netmask Tests

    assert iupy.v4_bits_to_mask('0') == "0.0.0.0", "/0 Netmask is wrong."
    assert iupy.v4_bits_to_mask('12') == "255.240.0.0", "/12 netmask is wrong."
    assert iupy.v4_bits_to_mask('24') == "255.255.255.0", "/24 Netmask is wrong."
    assert iupy.v4_bits_to_mask('32') == "255.255.255.255", "/32 Netmask is wrong."

    assert iupy.v4_bits_to_mask('-1') is None, "Bad bit value should return None."
    assert iupy.v4_bits_to_mask('33') is None, "Bad bit value should return None."

    # Wildcard Tests

    assert iupy.v4_wildcard('0') == "255.255.255.255", "Wildcard 0 is wrong."
    assert iupy.v4_wildcard('24') == "0.0.0.255", "Wildcard 24 is wrong."
    assert iupy.v4_wildcard('32') == "0.0.0.0", "Wildcard 32 is wrong."

    assert iupy.v4_wildcard('0.0.1.0') == "255.255.254.255", "Wildcard is wrong for 0.0.1.0."
    assert iupy.v4_wildcard('0.0.0.0') == "255.255.255.255", "Wildcard is wrong for 0.0.0.0.."
    assert iupy.v4_wildcard('4.2.2.1') == "251.253.253.254", "Wildcard is wrong for 4.2.2.1"
    assert iupy.v4_wildcard('255.255.255.0') == "0.0.0.255", "Wildcard is wrong for 255.255.255.0"
    assert iupy.v4_wildcard('255.255.255.256') is None, "Bad mask should return None."

    assert iupy.v4_wildcard(iupy.v4_wildcard("255.192.224.5")) == "255.192.224.5", "Double Wildcard should be equal."

    # All good if we have gotten this far!

    print("iupy/network tests passed!")
