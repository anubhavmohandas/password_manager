from cryptography.fernet import Fernet
import csv
import pyfiglet
import os

title = pyfiglet.figlet_format("W A R D E N")


try:
    with open("main.key", "rb") as key_file:
        key = key_file.read()
except:
    key = Fernet.generate_key()
    with open("main.key", "wb") as key_file:
        key_file.write(key)

# Encrypt the password using the key
def encrypt(key, password):
    password_key = Fernet(key)
    encrypted_password = password_key.encrypt(password.encode())
    return encrypted_password

# Decrypt the password using the key
def decrypt(key, encrypted_password):
    password_key = Fernet(key)
    decrypted_password = password_key.decrypt(encrypted_password).decode()
    return decrypted_password

# Save the encrypted password to the CSV file
def save_password(platform, encrypted_password):
    with open("passwords.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([platform, encrypted_password.decode()])

# Search for the platform and retrieve the encrypted password
def search(platform):
    with open("passwords.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            platform_name, encrypted_password = row
            if platform_name == platform:
                return encrypted_password.encode()
        else:
            return None

# Main menu loop
while True:
    print(title)
    print("1. Save to Warden")
    print("2. View Password")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        platform = input("Enter the platform name: ")
        password = input("Enter the password: ")
        encrypted_password = encrypt(key, password)
        save_password(platform, encrypted_password)
        print("Password encrypted and saved. \n")

    elif choice == "2":
        platform = input("Enter the platform name: ")
        encrypted_password = search(platform)
        if encrypted_password:
            decryption_key = input("Enter the decryption key: ")
            decrypted_password = decrypt(decryption_key, encrypted_password)
            print(f"Decrypted Password: {decrypted_password} \n")
        else:
            print("Platform not found. \n")
    elif choice == "0":
        print("Goodbye! \n")
        break
    else:
        print("Invalid choice. Please try again.")
