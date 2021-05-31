from cryptography.fernet import Fernet
import pathlib


def make_key(keypath: str = None):
    '''
    Generates a key, optionally write it to file.
    '''
    key = Fernet.generate_key()

    if keypath:
        with open(keypath, mode='wb') as f:
            f.write(key)
        print(f"Saved key to file: {keypath}")
    return key


def load_key(keypath: str) -> bytes:
    '''
    Load key from file
    '''
    return open(keypath, mode='rb').read()


def encrypt_file(key: bytes, input: str, output: str = None):
    '''
    Encrypted a file, given key, input path, and optional output path.
    '''

    fernet = Fernet(key)

    with open(input, mode='rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)

    if output is None or output == "":
        outputPathObj = pathlib.Path(input)
        output = str(outputPathObj.parent / f"{outputPathObj.stem}_encrypted{outputPathObj.suffix}")

    with open(output, mode='wb') as file:
        file.write(encrypted)

    print(f"Created encrypted file at: {output}")
    return output


def decrypt_file(key: bytes, input: str, output: str = None):
    '''
    Descrypt a file, given key, input path, and optional output path.
    '''

    fernet = Fernet(key)
    with open(input, mode='rb') as file:
        encrypted = file.read()

    if not output:
        outputPathObj = pathlib.Path(input)
        output = str(outputPathObj.parent / f"{outputPathObj.stem}_decrypted{outputPathObj.suffix}")

    decrypted = fernet.decrypt(encrypted)
    with open(output, mode='wb') as file:
        file.write(decrypted)
