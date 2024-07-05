"""
    ulid_flake/base32
    ~~~~~~~~~~~

    Base32 encoding and decoding for Ulid-Flake.
"""

ENCODING = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def encode(value, length):
    """Encode a value to a Base32 string with a specified length."""
    return ''.join([ENCODING[(value >> (5 * i)) & 31] for i in range(length-1, -1, -1)])


def decode(encoded):
    """Decode a Base32 string to a numeric value."""
    value = 0
    for char in encoded:
        value = value * 32 + ENCODING.index(char)
    return value
