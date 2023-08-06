from typing import Any
from MyCaesarCipher.main import CaesarCipher


class CaesarCipherTesting:
    """Provides methods for testing the encryption and decryption functionality of the `CaesarCipher` class.

    ---

    Contains the following test methods:

        - :func:`test_encrypt(self, text: str, key: int, assertion: str, output_results: bool = True) -> None`
            - Test encryption process using given text and shift-key.
            - Output of test results to stdout enabled by default.

        - :func:`test_decrypt(self, text: str, assertion: str, output_results: bool = True) -> None`
            - Test decryption method using given text.
            - Output of test results to stdout enabled by default.
    """

    def __init__(self, test_class=CaesarCipher()) -> None:
        self.test_class: Any = test_class

    def test_encrypt(
        self,
        text: str,
        key: int,
        assertion: str,
        output_results: bool = True,
    ) -> None:
        """
        Test encryption method using given text and shift-key.

        ---

        :param text: text to encrypt
        :type text: :class:`str`
        :param key: key to use for encryption
        :type key: :class:`str` | `None`
        :param assertion: expected output of the encryption
        :type assertion: :class:`str`
        :param output_results: toggle result output, defaults to :bool:`True`
        :type output_results: :class:`bool`, optional
        :return: result of encryption test
        :rtype: None
        """

        assert self.test_class.encrypt(text, key, output_results) == assertion

    def test_decrypt(self,
                     text: str,
                     assertion: str,
                     output_results: bool = True) -> None:
        """
        Test decryption method using given text.

        ---

        :param text: text to be decrypted
        :type text: :class:`str`
        :param assertion: expected result to be found within output
        :type assertion: :class:`str`
        :param output_results: toggle output of results to `stdout`, defaults to `False`
        :type output_results: :class:`bool`, optional
        :return: result of decryption test
        :rtype: None
        """

        assert assertion in self.test_class.decrypt(text, output_results)


# Create test class instance
testCC: CaesarCipherTesting = CaesarCipherTesting()


# Test encryption of string containing uppercase characters
def test_encodeA() -> None:
    testCC.test_encrypt('TESTING', 5, 'YJXYNSL')


# Test encryption of string containing both lowercase and uppercase characters
def test_encodeB() -> None:
    testCC.test_encrypt("TeStInG", 5, 'YjXyNsL')


# Test encryption of string containing digits
def test_encodeC() -> None:
    testCC.test_encrypt('16', 5, '61')


# Test encryption of string containing lowercase/uppercase characters and digits
def test_encodeD() -> None:
    testCC.test_encrypt("Password123", 5, 'Ufxxbtwi678', False)


# Test decryption of string containing lowercase characters
def test_decodeA() -> None:
    testCC.test_decrypt('djjktcqttccwprztsd', 'syyzirfiirrlegoihs')


# Test decryption of string containing lowercase/uppercase characters and digits
def test_decodeB() -> None:
    testCC.test_decrypt('2EkkLudRuuddXosaute123', '1DjjKtcQttccWnrztsd012')


# Test decryption of string containing lowercase/uppercase characters and punctuation
def test_decodeC() -> None:
    testCC.test_decrypt('Szh\'d te rztyr? Hlye ez slyr zfe zc dzxpestyr?',
                        'How\'s it going? Want to hang out or something?')


# Test decryption of string containing lowercase/uppercase characters, numbers and punctuation
def test_decodeD() -> None:
    testCC.test_decrypt('3120854 - Idbbn Ijidct', '8675309 - Tommy Tutone')
