from typing import Union
from file_encryption import *


def _cli_select_function():
    print("Select function: 1 - generate key; 2 - encrypt; 3 - decrypt; default: Exit")
    response = input().strip()
    if bool(response) is False:
        print("Goodbye.")
        sys.exit(0)

    if int(response) not in [1, 2, 3]:
        print("Unrecogized command.")
    else:
        return int(response)


def _cli_input_string(msg: str = None, default: str = None):
    if msg:
        print(msg)
    response = input().strip()

    if response:
        return response
    elif default:
        return default
    else:
        return response


def _cli_input_bool(msg: str = None, default: bool = None):

    if default is True:
        defaultSelections = '[Y/n]'
    elif default is False:
        defaultSelections = '[y/N]'
    else:
        defaultSelections = '[y/n]'

    if msg:
        print(f"{msg} {defaultSelections}")
    response = input().strip().lower()
    if response == '' and default is not None:
        return default
    elif response in ['y', 'n']:
        return response == 'y'
    else:
        print("Unrecognized command.")


def _cli_should_use_key_in_memory(useKeyInMemory: Union[bool, None] = None):
    while useKeyInMemory is None:
        useKeyInMemory = _cli_input_bool("Use the key that was just created?", default=True)
    return useKeyInMemory


def _cli_should_use_key_from_file(useKeyFromFile: Union[bool, None] = None):
    while useKeyFromFile is None:
        useKeyFromFile = _cli_input_bool("Load key from file?", default=True)
    return useKeyFromFile


def _cli_get_key_from_input(keyStr: Union[str, None] = None):
    while keyStr is None:
        keyStr = _cli_input_string("Enter a key:")
    key = keyStr.encode('utf-8')
    return key


def _cli_get_key_from_file_or_console(key: Union[bytes, None], useKeyInMemory: bool = False, keypath=None):
    if useKeyInMemory is False:
        useKeyFromFile = _cli_should_use_key_from_file()

        if useKeyFromFile is False:
            key = _cli_get_key_from_input()
        else:
            while keypath is None:
                keypath = _cli_input_string("File path to encryption key:")
            key = load_key(keypath)

    return key


def _cli_get_key(key: Union[bytes, None] = None):
    if key is not None:  # there is a key in memory
        useKeyInMemory = _cli_should_use_key_in_memory()
        key = _cli_get_key_from_file_or_console(key, useKeyInMemory)
    else:  # no key exist in memory
        key = _cli_get_key_from_file_or_console(key)
    return key


if __name__ == "__main__":
    import sys

    select: Union[int, None] = None
    key: Union[bytes, None] = None
    keypath: Union[str, None] = None
    fileToEncryptPath: Union[str, None] = None
    encryptedPath: Union[str, None] = None
    decryptOutputPath: Union[str, None] = None

    useKeyInMemory: Union[bool, None] = None
    useKeyFromFile: Union[bool, None] = None

    while True:

        select = _cli_select_function()

        if select == 1:
            keypath = _cli_input_string("Input file path to write key to: (Hit [enter/return] to skip).")
            key = make_key(keypath)
            print(f"Loaded key into memory: {key}")

        elif select == 2:
            key = _cli_get_key(key)

            while fileToEncryptPath is None:
                fileToEncryptPath = _cli_input_string("Path to file to be encrypted:")

            while encryptedPath is None:
                encryptedPath = _cli_input_string(
                    "Path to output encrypted file: (Hit [enter/return] to skip and save in same directory.)")

            if key:
                encryptedPath = encrypt_file(key, fileToEncryptPath, encryptedPath)

        elif select == 3:
            key = _cli_get_key(key)

            while encryptedPath is None:
                encryptedPath = _cli_input_string("Path to file to be decrypted:")

            while decryptOutputPath is None:
                decryptOutputPath = _cli_input_string(
                    "Path to output decrypted file: (Hit [enter/return] to skip and save in same directory.)")

            if key:
                print(f"encryptedPath={encryptedPath}")
                decrypt_file(key, encryptedPath, decryptOutputPath)
