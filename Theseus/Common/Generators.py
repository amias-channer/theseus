import os
import random
import mnemonic
import string
from pyblake2 import blake2b
import base58


def generate_mnemonic(language='english'):
    """ Generate Mnemonic: Creates insecure random nmemonics for testing

    Args:
        language (str): defaults to english , all bip languages are supported.

    Returns:
        (str): a list of mnemonic words separated by spaces

    Notes:
        These values MUST not be used for wallets with real ADA as they are
        not securely generated so could be predictable.
    """
    phrase_generator = mnemonic.Mnemonic(language)

    # make some insecure entropy
    strength_bits = 128
    entropy = os.urandom(strength_bits // 8)

    # make a phrase from it
    return phrase_generator.to_mnemonic(entropy)


def check_mnemonic(string, language='english'):
    """ Check menmonic: 

    Uses the python mnemonic library to check the supplied mnemonic is complies to the BIP-0039 standards

    Args:
        string(str): a list of mnemonic words seperated by spaces to be checked
        languge(str): a language to verify the mnemonic in , defaults to english
    """
    object = mnemonic.Mnemonic(language)
    return object.check(string)


def generate_walletname(evil=0, length=8):
    """ Generate Walletname: Creates wallet names of varying lengths and evilness

    Args:
        evil (int): 1 = alphanumeric , 2 = punctuation , 3 = any printable charecter
        length (int): length of wallet name

    Notes:

        Python string constants are used to create the charecter lists
        https://docs.python.org/3.4/library/string.html
    """
    string_options = str
    # configurable levels of evil content for wallet names
    if evil == 0:
        string_options = string.ascii_uppercase + string.digits
    if evil == 1:
        string_options = string.punctuation
    if evil == 2:
        string_options = string.printable

    return ''.join(random.choices(string_options, k=length))


def encode_spending_password(string):
    """" Create a blake2 hash and base58 encode it for use as a spending password

    Args:
        string(str): a string to encode as a password

    Returns:
          bytes: base58 encoding string
    """

    # might need to do some padding
    bl = blake2b(string.encode('utf-8'), digest_size=24)
    return base58.b58encode(bl.digest())


def generate_spending_password(evil=0, length=16):
    """" Generate a spending password and encode it

    Args:
        evil (int): 1 = alphanumeric , 2 = punctuation , 3 = any printable charecter
        length (int): length of wallet name

    Returns:
        bytes: base58 encoded password
    """
    return encode_spending_password(generate_walletname(evil=evil, length=length))