import hashlib

import os

def generate_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print("File not found.")
        return None
def main():
    print("🔐 File Integrity Checker 🔐")
    print("1. Generate and save file hash")
    print("2. Verify file integrity")
    choice = input("Choose an option (1 or 2): ").strip()

    file_path = input("\nEnter the full path of the file: ").strip('"')
    filename = os.path.basename(file_path)
    hash_result = generate_file_hash(file_path)

    if not hash_result:
        return

    if choice == "1":
        print(f"\nSHA-256 Hash:\n{hash_result}")
        try:
            with open("hashes.txt", "a") as log:
                log.write(f"{filename}: {hash_result}\n")
            print("\n✅ Hash saved to hashes.txt")
        except Exception as e:
            print("❌ Error saving hash:", e)

    elif choice == "2":
        try:
            with open("hashes.txt", "r") as log:
                lines = log.readlines()
                stored_hash = None

                for line in lines:
                    if line.startswith(filename + ":"):
                        stored_hash = line.strip().split(": ")[1]
                        break

                if stored_hash:
                    if stored_hash == hash_result:
                        print("\n✅ File integrity confirmed: No changes detected.")
                    else:
                        print("\n⚠️ WARNING: File has been modified or corrupted!")
                else:
                    print("\n❓ No saved hash found for this file.")
        except FileNotFoundError:
            print("\n❌ hashes.txt not found. Nothing to compare against.")

    else:
        print("\nInvalid choice. Please enter 1 or 2.")
main()
