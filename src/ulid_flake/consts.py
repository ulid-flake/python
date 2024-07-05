"""
    ulid_flake/consts
    ~~~~~~~~~~~

    Constants for Ulid-Flake.
"""
from datetime import datetime, timezone

DEFAULT_EPOCH = datetime(2024, 1, 1, tzinfo=timezone.utc)
MAX_TIMESTAMP = (1 << 43) - 1  # 43-bit maximum value
MAX_RANDOMNESS = (1 << 20) - 1  # 20-bit maximum value
MAX_RANDOMNESS_SCALABLE = (1 << 15) - 1  # 15-bit maximum value for scalable version
MAX_SCALABILITY = (1 << 5) - 1  # 5-bit maximum value
DEFAULT_ENTROPY_SIZE = 1  # Default entropy size (1 byte)
MAX_ENTROPY_SIZE = 3  # Max entropy size (3 byte)
MAX_ENTROPY_SIZE_SCALABLE = 2  # Max entropy size (2 byte) for scalable version
