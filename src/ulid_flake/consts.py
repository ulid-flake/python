"""
    ulid_flake/consts
    ~~~~~~~~~~~

    Constants for Ulid-Flake.
"""
from datetime import datetime, timezone

DEFAULT_EPOCH = datetime(2024, 1, 1, tzinfo=timezone.utc)

MIN_INT = int(0)  # 64-bit signed integer possible minimum value for Ulid-Flake (0)
MAX_INT = (1 << 63) - 1  # 64-bit signed integer possible maximum value for Ulid-Flake (9223372036854775807)

MIN_TIMESTAMP = int(0)  # 43-bit minimum value (0)
MAX_TIMESTAMP = (1 << 43) - 1  # 43-bit maximum value (8796093022207)

MIN_RANDOMNESS = int(0)  # 20-bit minimum value (0)
MAX_RANDOMNESS = (1 << 20) - 1  # 20-bit maximum value (1048575)
MAX_RANDOMNESS_SCALABLE = (1 << 15) - 1  # 15-bit maximum value for scalable version (32767)

MIN_ENTROPY_SIZE = int(1)  # Minimum entropy size (1 byte)
MAX_ENTROPY_SIZE = int(3)  # Maximum entropy size (3 byte)
MAX_ENTROPY_SIZE_SCALABLE = int(2)  # Maximum entropy size for scalable version (2 byte)

MIN_SCALABILITY = int(0)  # 5-bit minimum value for scalable version (0)
MAX_SCALABILITY = (1 << 5) - 1  # 5-bit maximum value for scalable version (31)

ULID_FLAKE_LEN = int(13)  # Length of Ulid-Flake string
MIN_ULID_FLAKE = "0000000000000"  # Minimum possible Ulid-Flake value (0)
MAX_ULID_FLAKE = "7ZZZZZZZZZZZZ"  # Maximum possible Ulid-Flake value (9223372036854775807)
