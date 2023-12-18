from cryptography.fernet import Fernet
from typing import Tuple


class log_encrypt:
    """A class to encrypt and decrypt the logs."""

    def __init__(self, logpath) -> None:
        self.path = logpath

    def generate_key():
        return Fernet.generate_key()

    def encrypt_file(file_path, key):
        """
        A function to encrypt a log by AES.
        After the encryption, the encrypted file will be saved in a new path "file_path + '.encrypted.log'", in which the "file path" is a parameter of the function.
        The function will return the new file path.
        """
        with open(file_path, "rb") as file:
            data = file.read()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        encrypted_file_path = file_path + ".encrypted.log"
        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        return encrypted_file_path

    def decrypt_file(encrypted_file_path, key) -> str:
        """
        A function to decrypt a log by AES.
        After the decryption, the decrypted file will be saved in a new path "encrypted_file_path + '.decrypted.log'", in which the "encrypted_file_path" is a parameter of the function.
        The function will return the new file path.
        """
        with open(encrypted_file_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        decrypted_file_path = encrypted_file_path + ".decrypted.log"
        with open(decrypted_file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
        return decrypted_file_path

    def log_safe(self, log_path) -> Tuple[str, str]:
        """
        A function to run the encrypt_file and decrypt_file function.
        Args:
            log_path (str)
        Returns:
            encrypted_file_path,decrypted_file_path
        """
        logpath = log_path
        key = self.generate_key()
        encrypted_file_path = self.encrypt_file(logpath, key)
        decrypted_file_path = self.decrypt_file(encrypted_file_path, key)
        return (encrypted_file_path, decrypted_file_path)
