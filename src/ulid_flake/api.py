"""
    ulid_flake/ulid_flake
    ~~~~~~~~~~~

    Ulid-Flake implementation.
"""
import os
import threading
from datetime import datetime, timezone
from .consts import DEFAULT_EPOCH, MAX_TIMESTAMP, MAX_RANDOMNESS, DEFAULT_ENTROPY_SIZE, MAX_ENTROPY_SIZE
from . import base32


class UlidFlake:
    epoch_time = DEFAULT_EPOCH
    entropy_size = DEFAULT_ENTROPY_SIZE
    previous_timestamp = None
    previous_randomness = None
    lock = threading.Lock()

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.base32

    @property
    def int(self):
        return self.value

    @property
    def hex(self):
        return hex(self.value)

    @property
    def bin(self):
        return bin(self.value)

    @property
    def base32(self):
        return base32.encode(self.value, 13)

    @property
    def timestamp(self):
        return (self.value >> 20) & MAX_TIMESTAMP

    @property
    def randomness(self):
        return self.value & MAX_RANDOMNESS

    @classmethod
    def set_config(cls, epoch_time=DEFAULT_EPOCH, entropy_size=DEFAULT_ENTROPY_SIZE):
        if entropy_size <= 0 or entropy_size > MAX_ENTROPY_SIZE:
            raise ValueError(f"Entropy size must be between 1 and {MAX_ENTROPY_SIZE}.")

        cls.epoch_time = epoch_time
        cls.entropy_size = entropy_size

    @classmethod
    def reset_config(self):
        self.epoch_time = DEFAULT_EPOCH
        self.entropy_size = DEFAULT_ENTROPY_SIZE

    @classmethod
    def generate_timestamp(cls):
        """Generate a 43-bit timestamp (milliseconds since Ulid-Flake epoch)."""
        timestamp = int((datetime.now(timezone.utc) - cls.epoch_time).total_seconds() * 1000)
        if timestamp > MAX_TIMESTAMP:
            raise OverflowError("Timestamp exceeds maximum Ulid-Flake value.")
        return timestamp

    @classmethod
    def generate_randomness(cls):
        """Generate a 20-bit randomness value."""
        return int.from_bytes(os.urandom(3), byteorder="big") & MAX_RANDOMNESS

    @classmethod
    def generate_entropy(cls, size=DEFAULT_ENTROPY_SIZE):
        """Generate an entropy value to increment randomness."""
        if size <= 0 or size > MAX_ENTROPY_SIZE:  # Ensure entropy size is within a reasonable range
            raise ValueError(f"Entropy size must be between 1 and {MAX_ENTROPY_SIZE}.")
        return int.from_bytes(os.urandom(size), byteorder="big")

    @classmethod
    def new(cls):
        """Generate a 64-bit signed Ulid-Flake with 43-bit timestamp and 20-bit randomness."""
        with cls.lock:
            timestamp = cls.generate_timestamp()

            if timestamp == cls.previous_timestamp:
                entropy = cls.generate_entropy(cls.entropy_size)
                while entropy <= 0:
                    entropy = cls.generate_entropy(cls.entropy_size)
                new_randomness = (cls.previous_randomness + entropy)
                if new_randomness > MAX_RANDOMNESS:
                    raise OverflowError("Randomness exceeds maximum ULID value.")
                randomness = new_randomness
            else:
                randomness = cls.generate_randomness()

            cls.previous_timestamp = timestamp
            cls.previous_randomness = randomness

            # Set the sign bit to 0 (positive)
            sign_bit = 0

            # Combine the sign bit, timestamp, and randomness
            combined = (sign_bit << 63) | (timestamp << 20) | randomness

            return cls(combined)

    @classmethod
    def parse(cls, ulid_flake_string):
        """Parse a Ulid-Flake string to create a Ulid-Flake instance."""
        if len(ulid_flake_string) != 13:
            raise ValueError("Ulid-Flake string must be 13 characters long.")
        try:
            value = base32.decode(ulid_flake_string.upper())
        except ValueError:
            raise ValueError("Ulid-Flake string contains invalid Base32 characters.")

        return cls(value)

    @classmethod
    def from_int(cls, value):
        """Create a Ulid-Flake instance from an integer."""
        return cls(value)

    @classmethod
    def from_str(cls, ulid_flake_string):
        """Create a Ulid-Flake instance from a Base32 string."""
        return cls.parse(ulid_flake_string)

    @classmethod
    def from_unix_epoch_time(cls, unix_time):
        """Create a Ulid-Flake instance from a Unix epoch time."""
        if not isinstance(unix_time, (int, float)):
            raise ValueError("unix_time must be an integer or float representing seconds since Unix epoch.")

        if unix_time < cls.epoch_time.timestamp():
            raise ValueError("Unix timestamp is before the custom epoch time.")

        timestamp = int((datetime.fromtimestamp(unix_time, tz=timezone.utc) - cls.epoch_time).total_seconds() * 1000)
        if timestamp > MAX_TIMESTAMP:
            raise OverflowError("Timestamp exceeds maximum Ulid-Flake value.")

        randomness = cls.generate_randomness()
        sign_bit = 0
        combined = (sign_bit << 63) | (timestamp << 20) | randomness
        return cls(combined)
