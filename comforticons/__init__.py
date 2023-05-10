"""ComfortIcons is an identicon generation module for different identicon/icon/gravatar/avatar flavors"""

from .main import Identicon
from . import preprocessors, generators

__all__ = [
    "Identicon",
    "generators",
    "preprocessors",
]