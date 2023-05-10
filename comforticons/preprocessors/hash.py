"""Hash data preprocessors module"""
from __future__ import annotations

import hashlib


from .base import BasePreprocessor


class HashPreprocessor(BasePreprocessor):
    """Hash data preprocessor

    :ivar hash_func: hash function
    :ivar encoding: data encoding
    :ivar entropy: entropy provided by hash function
    """

    def __init__(self, hash_func=hashlib.md5, encoding: str = "utf-8"):
        """Hash data preprocessor

        :param hash_func: hash function to use, defaults to hashlib.md5
        :type hash_func: Callable[[ReadableBuffer], _Hash], optional
        :param encoding: string encoding, defaults to "utf-8"
        :type encoding: str, optional
        """
        super().__init__()
        self.hash_func = hash_func
        self.encoding: str = encoding
        self.entropy: int = self.calc_entropy()

    def calc_entropy(self) -> int:
        """Calculate bit length (entropy) of self.hash_func

        Entropy is used for comparing provided entropy of hash function and required entropy of generator.

        :return: digest bit length, a.k.a entropy of hash_func
        :rtype: int
        """
        return len(self.hash_func("test".encode("utf-8")).hexdigest()) * 4

    def process(self, data: str) -> str:
        """Process data with self.hash_func

        :param data: data to process (usually an email or ip string)
        :type data: str
        :return: data hexdigest string
        :rtype: str
        """
        return self.hash_func(data.encode(self.encoding)).hexdigest()


class MD5Preprocessor(HashPreprocessor):
    """md5 data preprocessor"""

    def __init__(self, encoding: str = "utf-8"):
        """md5 data hash preprocessor

        :param encoding: string encoding, defaults to "utf-8"
        :type encoding: str, optional
        """
        super().__init__(hashlib.md5, encoding)


class SHA1Preprocessor(HashPreprocessor):
    """sha1 data preprocessor"""

    def __init__(self, encoding: str = "utf-8"):
        """sha1 data hash preprocessor

        :param encoding: string encoding, defaults to "utf-8"
        :type encoding: str, optional
        """
        super().__init__(hashlib.sha1, encoding)


__all__ = ["HashPreprocessor", "MD5Preprocessor", "SHA1Preprocessor"]
