"""Base data preprocessor interface module"""
from __future__ import annotations

from typing import Any


class BasePreprocessor:
    """Preprocessor interface

    Note: class has fixed entropy of 0!

    :ivar entropy: entropy provided by this data preprocessor
    """

    def __init__(self):
        """Preprocessor interface

        Note: class has fixed entropy of 0!
        """
        self.entropy = 0

    def check_data(self, data: str) -> None:
        """Check data before processing

        Note: Do not use directly, this class is an example/interface!

        :param data: Any
        :type data: str
        """
        raise NotImplementedError

    def process(self, data: Any) -> None:
        """Process data

        Note: Do not use directly, this class is an example/interface and will return None!

        :param data: data to process (usually an email or ip string)
        :type data: Any
        :return: example processed data
        :rtype: None
        """
        self.check_data(data)


__all__ = ["BasePreprocessor"]
