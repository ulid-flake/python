<h1 align="left">
	<img width="240" src="https://raw.githubusercontent.com/ulid-flake/spec/main/logo.png" alt="ulid-flake">
</h1>


# Ulid-Flake, A 64-bit ULID variant featuring Snowflake - the python implementation

Ulid-Flake is a compact `64-bit` ULID (Universally Unique Lexicographically Sortable Identifier) variant inspired by ULID and Twitter's Snowflake. It features a 1-bit sign bit, a 43-bit timestamp, and a 20-bit randomness. Additionally, it offers a scalable version using the last 5 bits as a scalability identifier (e.g., machineID, podID, nodeID).

herein is proposed Ulid-Flake:

```go
ulidflake.New() // 00CMXB6TAK4SA
ulidflake.New().Int() // 14246757444195114
```

## Features

- **Compact and Efficient**: Uses only 64 bits, making it compatible with common integer types like `int64` and `bigint`.
- **Scalability**: Provides 32 configurations for scalability using a distributed system.
- **Lexicographically Sortable**: Ensures lexicographical order.
- **Canonical Encoding**: Encoded as a 13-character string using Crockford's Base32.
- **Monotonicity and Randomness**: Monotonic sort order within the same millisecond with enhanced randomness to prevent predictability.

## Installation

To install Ulid-Flake, you can install via a package manager (if available):

```sh
pip install ulid-flake
```

or you can clone the repository:

```sh
git clone git@github.com:ulid-flake/python.git
```

## Basic Usage

```python
from ulid_flake.api import UlidFlake
from ulid_flake.scalable import UlidFlakeScalable
from datetime import datetime, timezone

# Configure settings for stand-alone version
UlidFlake.set_config(
    epoch_time=datetime(2024, 1, 1, tzinfo=timezone.utc),  # Custom epoch time, default 2024-01-01
    entropy_size=2,  # Custom entropy size, 1, 2 or 3, default 1
)

# Configure settings for scalable version
UlidFlakeScalable.set_config(
    epoch_time=datetime(2024, 1, 1, tzinfo=timezone.utc),  # Custom epoch time, default 2024-01-01
    entropy_size=2,  # Custom entropy size, 1 or 2, default 1
    sid=3  # Custom scalability ID (e.g., machineID, podID, nodeID), 1~32, default 0
)

# Generate a new Ulid-Flake ID instance
flake_id = UlidFlake.new()
print(f"flake_id: {flake_id}")
print(f"Timestamp: {flake_id.timestamp}")
print(f"Randomness: {flake_id.randomness}")
print(f"Base32: {flake_id.base32}")
print(f"Integer: {flake_id.int}")
print(f"Hex: {flake_id.hex}")
print(f"Binary: {flake_id.bin}")

# flake_id: 00EZJCRCB4650

# Timestamp: 16091865483
# Randomness: 4293

# Base32: 00EZJCRCB4650
# Integer: 16873543940839584
# Hex: 0x3bf26618b218a0
# Binary: 0b111011111100100110011000011000101100100001100010100000
```

## Monotonicity Testing

Stand-alone version:

```python
from ulid_flake.api import UlidFlake

for _ in range(5):
    flake_id = UlidFlake.new()
    print(f"Base32: {flake_id.base32}")
    print(f"BigInt: {flake_id.int}")
    print(f"Hex: {flake_id.hex}")
    print(f"Bin: {flake_id.bin}")

# Base32: 00EZJCRCBDKGC
# BigInt: 16873543941148172
# Hex: 0x3bf26618b6ce0c
# Bin: 0b111011111100100110011000011000101101101100111000001100

# Base32: 00EZJCRCBDKHZ
# BigInt: 16873543941148223
# Hex: 0x3bf26618b6ce3f
# Bin: 0b111011111100100110011000011000101101101100111000111111

# Base32: 00EZJCRCBDKPZ
# BigInt: 16873543941148383
# Hex: 0x3bf26618b6cedf
# Bin: 0b111011111100100110011000011000101101101100111011011111

# Base32: 00EZJCRCBDKWA
# BigInt: 16873543941148554
# Hex: 0x3bf26618b6cf8a
# Bin: 0b111011111100100110011000011000101101101100111110001010

# Base32: 00EZJCRCBDKWG
# BigInt: 16873543941148560
# Hex: 0x3bf26618b6cf90
# Bin: 0b111011111100100110011000011000101101101100111110010000
```

scalable version:

```python
from ulid_flake.scalable import UlidFlakeScalable

UlidFlakeScalable.set_config(sid=2)
for _ in range(5):
    flake_id = UlidFlakeScalable.new()
    print(f"Base32: {flake_id.base32}")
    print(f"BigInt: {flake_id.int}")
    print(f"Hex: {flake_id.hex}")
    print(f"Bin: {flake_id.bin}")

# Base32: 00EZJCRCB4B32
# BigInt: 16873543940844642
# Hex: 0x3bf26618b22c62
# Bin: 0b111011111100100110011000011000101100100010110001100010

# Base32: 00EZJCRCB4F22
# BigInt: 16873543940848706
# Hex: 0x3bf26618b23c42
# Bin: 0b111011111100100110011000011000101100100011110001000010

# Base32: 00EZJCRCB4GP2
# BigInt: 16873543940850370
# Hex: 0x3bf26618b242c2
# Bin: 0b111011111100100110011000011000101100100100001011000010

# Base32: 00EZJCRCB4PM2
# BigInt: 16873543940856450
# Hex: 0x3bf26618b25a82
# Bin: 0b111011111100100110011000011000101100100101101010000010

# Base32: 00EZJCRCB4V02
# BigInt: 16873543940860930
# Hex: 0x3bf26618b26c02
# Bin: 0b111011111100100110011000011000101100100110110000000010
```

## Creating Ulid-Flake Instances from other sources

### From Integer

```python
ulid_flake_from_int = UlidFlake.from_int(1234567890123456789)
print(f"From Int: {ulid_flake_from_int}")
```

### From Base32 String

```python
ulid_flake_from_str = UlidFlake.from_str("01AN4Z07BY79K")
print(f"From String: {ulid_flake_from_str}")
```

### From Unix Epoch Time

```python

ulid_flake_from_unix = UlidFlake.from_unix_epoch_time(1720159853432)
print(f"From Unix Time: {ulid_flake_from_unix}")
```

## Specification

Below is the default stand-alone version specification of Ulid-Flake.

<img width="600" alt="ulid-flake-stand-alone" src="https://github.com/ulid-flake/spec/assets/38312944/37d44c3f-1937-4c2e-b7ec-e7c0f0debe25">

*Note: a `1-bit` sign bit is included in the timestamp.*

```text
Stand-alone version (default):

 00CMXB6TA      K4SA

|---------|    |----|
 Timestamp   Randomness
   44-bit      20-bit
   9-char      4-char
```

Also, a scalable version is provided for distributed system using purpose.

<img width="600" alt="ulid-flake-scalable" src="https://github.com/ulid-flake/spec/assets/38312944/e306ebd9-9406-436f-b6cd-a1004745f1b0">

*Note: a `1-bit` sign bit is included in the timestamp.*

```
Scalable version (optional):

 00CMXB6TA      K4S       A

|---------|    |---|     |-|
 Timestamp   Randomness  Scalability
   44-bit      15-bit    5-bit
   9-char      3-char    1-char
```

### Components

Total `64-bit` size for compatibility with common integer (`long int`, `int64` or `bigint`) types.

**Timestamp**
- The first `1-bit` is a sign bit, always set to 0.
- Remaining `43-bit` timestamp in millisecond precision.
- Custom epoch for extended usage span, starting from `2024-01-01T00:00:00.000Z`.
- Usable until approximately `2302-09-27` AD.

**Randomness**
- `20-bit` randomness for stand-alone version. Provides a collision resistance with a p=0.5 expectation of 1,024 trials. (not much)
- `15-bit` randomness for scalable version.
- Initial random value at each millisecond precision unit.
- adopt a `+n` bits entropy incremental mechanism to ensure uniqueness without predictability.

**Scalability (Scalable version ony)**
- Provide a `5-bit` scalability for distributed system using purpose.
- total 32 configurations can be used.

### Sorting

The left-most character must be sorted first, and the right-most character sorted last, ensuring lexicographical order.
The default ASCII character set must be used.

When using the stand-alone version strictly in a stand-alone environment, or using the scalable version in both stand-alone or distributed environment, sort order is guaranteed within the same millisecond. however, when using the stand-alone version in a distributed system, sort order is not guaranteed within the same millisecond.

*Note: within the same millisecond, sort order is guaranteed in the context of an overflow error could occur.*

### Canonical String Representation

```text
Stand-alone version (default):

tttttttttrrrr

where
t is Timestamp (9 characters)
r is Randomness (4 characters)
```

```text
Scalable version (optional):

tttttttttrrrs

where
t is Timestamp (9 characters)
r is Randomness (3 characters)
s is Scalability (1 characters)
```

#### Encoding

Crockford's Base32 is used as shown. This alphabet excludes the letters I, L, O, and U to avoid confusion and abuse.

```
0123456789ABCDEFGHJKMNPQRSTVWXYZ
```

### Optional Long Int Representation

```text
1234567890123456789

(with a maximum 13-character length in string format)
```

### Monotonicity and Overflow Error Handling

#### Randomness

When generating a Ulid-Flake within the same millisecond, the `randomness` component is incremented by a `n-bit` entropy in the least significant bit position (with carrying).
Thus, comparing just incremented `1-bit` one time, the incremented `n-bit` mechanism cloud lead to an overflow error sooner.

when the generation is failed with overflow error, it should be properly handled in the application to wait and create a new one till the next millisecond is coming. The implementation of Ulid-Flake should just return the overflow error, and leave the rest to the application.

#### Timestamp and Over All

Technically, a `13-character` Base32 encoded string can contain 65 bits of information, whereas a Ulid-Flake must only contain 64 bits. Further more, there is a `1-bit` sign bit at the beginning, only 63 bits are actually carrying effective information. Therefore, the largest valid Ulid-Flake encoded in Base32 is `7ZZZZZZZZZZZZ`, which corresponds to an epoch time of `8,796,093,022,207` or `2^43 - 1`.

Any attempt to decode or encode a Ulid-Flake larger than this should be rejected by all implementations and return an overflow error, to prevent overflow bugs.

### Binary Layout and Byte Order

The components are encoded as 16 octets. Each component is encoded with the Most Significant Byte first (network byte order).

```
Stand-alone version (default):

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      32_bit_int_time_high                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| 12_bit_uint_time_low  |          20_bit_uint_random           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

```
Scalable version (optional):

 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      32_bit_int_time_high                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| 12_bit_uint_time_low  |      15_bit_uint_random     | 5_bit_s |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

# Contributing
We welcome contributions! Please see our CONTRIBUTING.md for guidelines on how to get involved.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments

[ULID](https://github.com/ulid/spec)

[Twitter's Snowflake](https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake)

```
██╗░░░██╗██╗░░░░░██╗██████╗░░░░░░░███████╗██╗░░░░░░█████╗░██╗░░██╗███████╗
██║░░░██║██║░░░░░██║██╔══██╗░░░░░░██╔════╝██║░░░░░██╔══██╗██║░██╔╝██╔════╝
██║░░░██║██║░░░░░██║██║░░██║█████╗█████╗░░██║░░░░░███████║█████═╝░█████╗░░
██║░░░██║██║░░░░░██║██║░░██║╚════╝██╔══╝░░██║░░░░░██╔══██║██╔═██╗░██╔══╝░░
╚██████╔╝███████╗██║██████╔╝░░░░░░██║░░░░░███████╗██║░░██║██║░╚██╗███████╗
░╚═════╝░╚══════╝╚═╝╚═════╝░░░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝
```
