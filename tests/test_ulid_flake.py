#!/usr/bin/env python

"""Tests for `ulid_flake` package."""


import unittest
from datetime import datetime, timezone, timedelta

from ulid_flake.ulid_flake import UlidFlake
from ulid_flake.ulid_flake_scalable import UlidFlakeScalable


class TestUlidFlake(unittest.TestCase):
    """Tests for `ulid_flake` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_generate_ulid_flake(self):
        """Test Generate Ulid-Flake"""
        ulid_flake = UlidFlake.new()
        self.assertIsInstance(ulid_flake, UlidFlake)
        self.assertEqual(len(str(ulid_flake)), 13)
        self.assertEqual(len(ulid_flake.base32), 13)
        self.assertEqual(len(ulid_flake.hex), 16)
        self.assertGreaterEqual(len(ulid_flake.bin), 56)

    def test_generate_ulid_flake_with_entropy(self):
        """Test Generate Ulid-Flake with Entropy"""
        UlidFlake.set_config(entropy_size=2)
        ulid_flake_id = UlidFlake.new()
        self.assertIsInstance(ulid_flake_id, UlidFlake)
        self.assertEqual(len(str(ulid_flake_id)), 13)
        self.assertEqual(len(ulid_flake_id.base32), 13)
        self.assertEqual(len(ulid_flake_id.hex), 16)
        self.assertGreaterEqual(len(ulid_flake_id.bin), 56)
        UlidFlake.reset_config()

    def test_generate_ulid_flake_with_out_of_range_entropy_size(self):
        """Test Generate Ulid-Flake with Large Entropy"""
        with self.assertRaises(ValueError):
            UlidFlake.set_config(entropy_size=0)
        UlidFlake.reset_config()

        with self.assertRaises(ValueError):
            UlidFlake.set_config(entropy_size=4)
        UlidFlake.reset_config()

    def test_generate_ulid_flake_with_large_entropy(self):
        """Test Generate Ulid-Flake with Large Entropy"""
        # after only 2 or 3 rounds, the entropy size will become too large
        UlidFlake.set_config(entropy_size=3)
        with self.assertRaises(OverflowError):
            for _ in range(3):
                UlidFlake.new()
        UlidFlake.reset_config()

    def test_parse_ulid_flake(self):
        """Test Parse Ulid-Flake"""
        ulid_flake = UlidFlake.new()
        parsed_ulid_flake = UlidFlake.parse(ulid_flake.base32)
        self.assertEqual(ulid_flake.value, parsed_ulid_flake.value)
        self.assertEqual(ulid_flake.timestamp, parsed_ulid_flake.timestamp)
        self.assertEqual(ulid_flake.randomness, parsed_ulid_flake.randomness)

    def test_parse_ulid_flake_with_invalid_base32(self):
        """Test Parse Ulid-Flake with Invalid Base32"""

        # invalid base32 string format
        with self.assertRaises(ValueError):
            UlidFlake.parse("invalid-base32")

        # invalid base32 characters I
        with self.assertRaises(ValueError):
            UlidFlake.parse("00CMH8K1E1E1I")

        # invalid base32 characters L
        with self.assertRaises(ValueError):
            UlidFlake.parse("00CMH8K1E1E1L")

        # invalid base32 characters O
        with self.assertRaises(ValueError):
            UlidFlake.parse("00CMH8K1E1E1O")

        # invalid base32 characters U
        with self.assertRaises(ValueError):
            UlidFlake.parse("00CMH8K1E1E1U")

        # invalid base32 length
        with self.assertRaises(ValueError):
            UlidFlake.parse("00CMH8K1E")
        with self.assertRaises(ValueError):
            UlidFlake.parse("00CMH8K1E1E1E2")

    def test_monotonically_increasing_ulid_flake(self):
        """Test Monotonically Increasing Ulid-Flake"""
        ulid_flake_id = UlidFlake.new()
        for _ in range(100):
            new_ulid_flake = UlidFlake.new()
            self.assertGreater(new_ulid_flake.value, ulid_flake_id.value)
            ulid_flake_id = new_ulid_flake

    def test_create_ulid_flake_from_int(self):
        """Test Create Ulid-Flake from Integer"""
        ulid_flake = UlidFlake.new()
        ulid_flake_from_int = UlidFlake.from_int(ulid_flake.value)
        self.assertEqual(ulid_flake.value, ulid_flake_from_int.value)
        self.assertEqual(ulid_flake.timestamp, ulid_flake_from_int.timestamp)
        self.assertEqual(ulid_flake.randomness, ulid_flake_from_int.randomness)

    def test_create_ulid_flake_from_str(self):
        """Test Create Ulid-Flake from String"""
        ulid_flake = UlidFlake.new()
        ulid_flake_from_str = UlidFlake.from_str(ulid_flake.base32)
        self.assertEqual(ulid_flake.value, ulid_flake_from_str.value)
        self.assertEqual(ulid_flake.timestamp, ulid_flake_from_str.timestamp)
        self.assertEqual(ulid_flake.randomness, ulid_flake_from_str.randomness)

    def test_create_ulid_flake_from_unix_epoch_time(self):
        """Test Create Ulid-Flake from Unix Epoch Time"""
        custom_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        ulid_flake = UlidFlake.new()
        ulid_flake_timestamp = ulid_flake.timestamp
        unix_timestamp = (custom_epoch + timedelta(milliseconds=ulid_flake_timestamp)).timestamp()
        ulid_flake_from_unix_epoch_time = UlidFlake.from_unix_epoch_time(unix_timestamp)
        self.assertEqual(ulid_flake.timestamp, ulid_flake_from_unix_epoch_time.timestamp)
        self.assertNotEqual(ulid_flake.randomness, ulid_flake_from_unix_epoch_time.randomness)

    def test_create_ulid_flake_from_unix_epoch_time_before_custom_epoch(self):
        """Test Create Ulid-Flake from Unix Epoch Time Before Custom Epoch"""
        custom_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        ulid_flake = UlidFlake.new()
        ulid_flake_timestamp = ulid_flake.timestamp
        unix_timestamp = (custom_epoch - timedelta(milliseconds=ulid_flake_timestamp)).timestamp()
        with self.assertRaises(ValueError):
            UlidFlake.from_unix_epoch_time(unix_timestamp)

    def test_create_ulid_flake_from_unix_epoch_time_after_max_timestamp(self):
        """Test Create Ulid-Flake from Unix Epoch Time After Max Timestamp"""
        max_timestamp = (1 << 43) - 1  # 43-bit maximum value
        custom_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        unix_timestamp = (custom_epoch + timedelta(milliseconds=max_timestamp + 1)).timestamp()
        with self.assertRaises(OverflowError):
            UlidFlake.from_unix_epoch_time(unix_timestamp)

    def test_create_ulid_flake_from_unix_epoch_time_with_invalid_unix_time(self):
        """Test Create Ulid-Flake from Unix Epoch Time with Invalid Unix Time"""
        with self.assertRaises(ValueError):
            UlidFlake.from_unix_epoch_time("invalid-time")


class TestUlidFlakeScalable(unittest.TestCase):
    """Tests for `ulid_flake` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_generate_ulid_flake_scalable_with_entropy_and_sid(self):
        """Test Generate Ulid-Flake with Entropy and Scalability ID"""
        UlidFlakeScalable.set_config(entropy_size=1, sid=1)
        ulid_flake_scalable_id = UlidFlakeScalable.new()
        self.assertIsInstance(ulid_flake_scalable_id, UlidFlakeScalable)
        self.assertEqual(len(str(ulid_flake_scalable_id)), 13)
        self.assertEqual(len(ulid_flake_scalable_id.base32), 13)
        self.assertEqual(len(ulid_flake_scalable_id.hex), 16)
        self.assertGreaterEqual(len(ulid_flake_scalable_id.bin), 56)
        UlidFlake.reset_config()

    def test_generate_ulid_flake_scalable_with_large_sid(self):
        """Test Generate Ulid-Flake with Large Scalability ID"""
        with self.assertRaises(ValueError):
            UlidFlakeScalable.set_config(sid=32)
        UlidFlake.reset_config()

    def test_parse_ulid_flake_scalable(self):
        """Test Parse Ulid-Flake Scalable"""
        ulid_flake_scalable = UlidFlakeScalable.new()
        parsed_ulid_flake_scalable = UlidFlakeScalable.parse(ulid_flake_scalable.base32)
        self.assertEqual(ulid_flake_scalable.value, parsed_ulid_flake_scalable.value)
        self.assertEqual(ulid_flake_scalable.timestamp, parsed_ulid_flake_scalable.timestamp)
        self.assertEqual(ulid_flake_scalable.randomness, parsed_ulid_flake_scalable.randomness)
        self.assertEqual(ulid_flake_scalable.sid, parsed_ulid_flake_scalable.sid)

    def test_parse_ulid_flake_scalable_with_invalid_base32(self):
        """Test Parse Ulid-Flake Scalable with Invalid Base32"""

        # invalid base32 string format
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("invalid-base32")

        # invalid base32 characters I
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("00CMH8K1E1E1I")

        # invalid base32 characters L
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("00CMH8K1E1E1L")

        # invalid base32 characters O
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("00CMH8K1E1E1O")

        # invalid base32 characters U
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("00CMH8K1E1E1U")

        # invalid base32 length
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("00CMH8K1E")
        with self.assertRaises(ValueError):
            UlidFlakeScalable.parse("00CMH8K1E1E1E2")

    def test_monotonically_increasing_ulid_flake_scalable(self):
        """Test Monotonically Increasing Ulid-Flake Scalable"""
        ulid_flake_scalable = UlidFlakeScalable.new()
        for _ in range(5):
            new_ulid_flake_scalable = UlidFlakeScalable.new()
            self.assertGreater(new_ulid_flake_scalable.value, ulid_flake_scalable.value)
            ulid_flake_scalable = new_ulid_flake_scalable

    def test_create_ulid_flake_scalable_from_int(self):
        """Test Create Ulid-Flake from Integer"""
        ulid_flake = UlidFlakeScalable.new()
        ulid_flake_from_int = UlidFlakeScalable.from_int(ulid_flake.value)
        self.assertEqual(ulid_flake.value, ulid_flake_from_int.value)
        self.assertEqual(ulid_flake.timestamp, ulid_flake_from_int.timestamp)
        self.assertEqual(ulid_flake.randomness, ulid_flake_from_int.randomness)

    def test_create_ulid_flake_scalable_from_str(self):
        """Test Create Ulid-Flake from String"""
        ulid_flake = UlidFlakeScalable.new()
        ulid_flake_from_str = UlidFlakeScalable.from_str(ulid_flake.base32)
        self.assertEqual(ulid_flake.value, ulid_flake_from_str.value)
        self.assertEqual(ulid_flake.timestamp, ulid_flake_from_str.timestamp)
        self.assertEqual(ulid_flake.randomness, ulid_flake_from_str.randomness)

    def test_create_ulid_flake_scalable_from_unix_epoch_time(self):
        """Test Create Ulid-Flake from Unix Epoch Time"""
        custom_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        ulid_flake = UlidFlakeScalable.new()
        ulid_flake_timestamp = ulid_flake.timestamp
        unix_timestamp = (custom_epoch + timedelta(milliseconds=ulid_flake_timestamp)).timestamp()
        ulid_flake_from_unix_epoch_time = UlidFlakeScalable.from_unix_epoch_time(unix_timestamp)
        self.assertEqual(ulid_flake.timestamp, ulid_flake_from_unix_epoch_time.timestamp)
        self.assertNotEqual(ulid_flake.randomness, ulid_flake_from_unix_epoch_time.randomness)
        self.assertEqual(ulid_flake.sid, ulid_flake_from_unix_epoch_time.sid)

    def test_create_ulid_flake_scalable_from_unix_epoch_time_before_custom_epoch(self):
        """Test Create Ulid-Flake from Unix Epoch Time Before Custom Epoch"""
        custom_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        ulid_flake = UlidFlakeScalable.new()
        ulid_flake_timestamp = ulid_flake.timestamp
        unix_timestamp = (custom_epoch - timedelta(milliseconds=ulid_flake_timestamp)).timestamp()
        with self.assertRaises(ValueError):
            UlidFlakeScalable.from_unix_epoch_time(unix_timestamp)

    def test_create_ulid_flake_scalable_from_unix_epoch_time_after_max_timestamp(self):
        """Test Create Ulid-Flake from Unix Epoch Time After Max Timestamp"""
        max_timestamp = (1 << 43) - 1  # 43-bit maximum value
        custom_epoch = datetime(2024, 1, 1, tzinfo=timezone.utc)
        unix_timestamp = (custom_epoch + timedelta(milliseconds=max_timestamp + 1)).timestamp()
        with self.assertRaises(OverflowError):
            UlidFlakeScalable.from_unix_epoch_time(unix_timestamp)

    def test_create_ulid_flake_scalable_from_unix_epoch_time_with_invalid_unix_time(self):
        """Test Create Ulid-Flake from Unix Epoch Time with Invalid Unix Time"""
        with self.assertRaises(ValueError):
            UlidFlakeScalable.from_unix_epoch_time("invalid-time")
