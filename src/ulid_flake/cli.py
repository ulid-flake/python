"""
    ulid_flake/cli
    ~~~~~~~~~~~

    Command-line interface for Ulid-Flake.
"""
from ulid_flake.ulid_flake import UlidFlake
from ulid_flake.ulid_flake_scalable import UlidFlakeScalable

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main(n: int = 5, entropy: int = 1, sid: int = 0):
    ulid_flake_ascii = """
    ██╗░░░██╗██╗░░░░░██╗██████╗░░░░░░░███████╗██╗░░░░░░█████╗░██╗░░██╗███████╗
    ██║░░░██║██║░░░░░██║██╔══██╗░░░░░░██╔════╝██║░░░░░██╔══██╗██║░██╔╝██╔════╝
    ██║░░░██║██║░░░░░██║██║░░██║█████╗█████╗░░██║░░░░░███████║█████═╝░█████╗░░
    ██║░░░██║██║░░░░░██║██║░░██║╚════╝██╔══╝░░██║░░░░░██╔══██║██╔═██╗░██╔══╝░░
    ╚██████╔╝███████╗██║██████╔╝░░░░░░██║░░░░░███████╗██║░░██║██║░╚██╗███████╗
    ░╚═════╝░╚══════╝╚═╝╚═════╝░░░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝
    """
    print(ulid_flake_ascii)
    ulid_flake = UlidFlake.new()
    print(f"New Ulid-Flake: \n{ulid_flake}\n")
    print(f"Timestamp: {ulid_flake.timestamp}")
    print(f"Randomness: {ulid_flake.randomness}\n")
    print(f"Base32: {ulid_flake.base32}")
    print(f"Int: {ulid_flake.int}")
    print(f"Hex: {ulid_flake.hex}")
    print(f"Binary: {ulid_flake.bin}")

    print("\nMonotonically increasing testing:\n")
    UlidFlake.set_config(entropy_size=entropy)
    for _ in range(n):
        ulid_instance = UlidFlake.new()
        print(f"Generated ULID (Base32): {ulid_instance.base32}")
        print(f"Generated ULID (BigInt): {ulid_instance.int}")
        print(f"Generated ULID (Hex): {ulid_instance.hex}")
        print(f"Generated ULID (Bin): {ulid_instance.bin}")
        print()
    UlidFlake.reset_config()

    ulid_flake_ascii = """
    ██╗░░░██╗██╗░░░░░██╗██████╗░░░░░░░███████╗██╗░░░░░░█████╗░██╗░░██╗███████╗░░░░░░░██████╗
    ██║░░░██║██║░░░░░██║██╔══██╗░░░░░░██╔════╝██║░░░░░██╔══██╗██║░██╔╝██╔════╝░░░░░░██╔════╝
    ██║░░░██║██║░░░░░██║██║░░██║█████╗█████╗░░██║░░░░░███████║█████═╝░█████╗░░█████╗╚█████╗░
    ██║░░░██║██║░░░░░██║██║░░██║╚════╝██╔══╝░░██║░░░░░██╔══██║██╔═██╗░██╔══╝░░╚════╝░╚═══██╗
    ╚██████╔╝███████╗██║██████╔╝░░░░░░██║░░░░░███████╗██║░░██║██║░╚██╗███████╗░░░░░░██████╔╝
    ░╚═════╝░╚══════╝╚═╝╚═════╝░░░░░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝░░░░░░╚═════╝░
    """
    print(ulid_flake_ascii)
    ulid_flake = UlidFlakeScalable.new()
    print(f"New Ulid-Flake: \n{ulid_flake}\n")
    print(f"Timestamp: {ulid_flake.timestamp}")
    print(f"Randomness: {ulid_flake.randomness}\n")
    print(f"Base32: {ulid_flake.base32}")
    print(f"Int: {ulid_flake.int}")
    print(f"Hex: {ulid_flake.hex}")
    print(f"Binary: {ulid_flake.bin}")

    print("\nMonotonically increasing testing:\n")
    UlidFlakeScalable.set_config(entropy_size=entropy, sid=sid)
    for _ in range(n):
        ulid_instance = UlidFlakeScalable.new()
        print(f"Generated ULID (Base32): {ulid_instance.base32}")
        print(f"Generated ULID (BigInt): {ulid_instance.int}")
        print(f"Generated ULID (Hex): {ulid_instance.hex}")
        print(f"Generated ULID (Bin): {ulid_instance.bin}")
        print()
    UlidFlakeScalable.reset_config()


if __name__ == "__main__":
    app()
