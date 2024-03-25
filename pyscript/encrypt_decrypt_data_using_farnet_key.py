from cryptography.fernet import Fernet


def encrypt_payload(key, data):
    """
    The function encrypts data using a given key.
    
    :param key: The key is a secret key used for encryption. It should be a 32-byte string encoded in
    base64
    :param data: The `data` parameter is the string that you want to encrypt
    :return: The encrypted version of the data.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decrypt_payload(key, encrypted_data):
    """
    The function decrypts encrypted data using a given key.
    
    :param key: The key is a bytes-like object that is used to encrypt and decrypt the data. It should
    be a 32-byte URL-safe base64-encoded string
    :param encrypted_data: The encrypted data is the data that has been encoded using a specific
    encryption algorithm. It is a string of characters that cannot be understood or read without the
    correct decryption key
    :return: The decrypted data as a string.
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()