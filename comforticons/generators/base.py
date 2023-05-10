"""Base generator interface module"""
from __future__ import annotations


class BaseGenerator:
    """Avatar generator interface

    :ivar size: avatar features size (grid size, rings amount, etc)
    :ivar entropy: required entropy for this generator
    """

    def __init__(
        self,
        size: int,
    ):
        """Base generator interface

        Note: Entropy in this class defaults to None!

        :param size: avatar features size
        :type size: int
        """
        self.size: int = size
        self.entropy: int = None

    def check_entropy(self, provided_entropy: int) -> bool:
        """Entropy comparement function

        Compare generator required entropy with provided.

        :param provided_entropy: entropy provided by data preprocessor
        :type provided_entropy: int
        :return: entropy comparement result
        :rtype: bool
        """
        return provided_entropy >= self.entropy

    def generate(self, data: str, avatar_size: int) -> None:
        """Generate avatar

        Note: Do not use directly, this class is an example/interface and returns None!

        :param data: avatar data
        :type data: str
        :param avatar_size: generated avatar dimensions (image dimensions, width of ascii 'image')
        :type avatar_size: int
        :return: generated avatar
        :rtype: None
        """
        return None


__all__ = ["BaseGenerator"]
