"""Identicon class implementation"""
from __future__ import annotations

from .preprocessors.base import BasePreprocessor
from .preprocessors.hash import MD5Preprocessor

from .generators.base import BaseGenerator
from .generators.image import PixelGenerator

from typing import Any


class Identicon:
    """Factory class that can be used for deterministically generating
    avatars with `generator` based on passed data preprocessed by `preprocessors`.

    :ivar preprocessors: list of preprocessor instances to be used in generation
    :ivar generator: avatar generator instance to be used in the last step of generation
    :ivar check_entropy: boolean flag - require preprocessor provided entropy >= generator required entropy
    """

    def __init__(
        self,
        preprocessors: list[BasePreprocessor] = [MD5Preprocessor()],
        generator: BaseGenerator = PixelGenerator(),
        check_entropy: bool = True,
    ):
        """Constructor

        :param preprocessors: a list of data preprocessors, defaults to [MD5Preprocessor()]
        :type preprocessors: list[BasePreprocessor], optional
        :param generator: avatar generator, defaults to [PixelGenerator()]
        :type generator: BaseGenerator, optional
        """
        if generator is None:
            raise ValueError("Must specify generator or use default - PixelGenerator()")

        self.preprocessors = preprocessors or []
        self.generator = generator
        self.check_entropy = check_entropy

    def generate(self, data: Any) -> Any:
        """Generate avatar using specified preprocessors and generator

        :param data: data to be used in generation (usually an email or ip string)
        :type data: Any
        :raises ValueError: if entropy provided by last preprocessor is not sufficient for `generator` required entropy, will not be raised if `check_entropy` is False
        :return: generated avatar
        :rtype: Any
        """
        if self.preprocessors:
            last_preprocessor = self.preprocessors[-1]
            if self.check_entropy and not self.generator.check_entropy(
                last_preprocessor.entropy
            ):
                raise ValueError(
                    f"Entropy provided by preprocessor {last_preprocessor.__class__.__name__}: {last_preprocessor.entropy} is not sufficent for generator {self.generator.__class__.__name__}, minimal entropy {self.generator.entropy} required."
                )
            for preprocessor in self.preprocessors:
                data = preprocessor.process(data)
        return self.generator.generate(data)


__all__ = ["Identicon"]
