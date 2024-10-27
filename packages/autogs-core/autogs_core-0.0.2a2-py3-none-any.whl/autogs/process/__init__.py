"""
This module contains the functions to process text without using AI
"""

import re
from typing import List


def search(text: str, term: str) -> List[int]:
    """
    Search for a term in a text and return their start indexes
    Args:
        text: str: The text
        term: str: The term
    Returns:
        list: The indexes of the term in the text
    Examples:
        >>> search("hello world", "world")
        [6]
        >>> "hello world"[6:11]
        'world'
        >>> search("hello world, from the other side of the world", "world")
        [6, 40]
        >>> "hello world, from the other side of the world"[6:11]
        'world'
        >>> "hello world, from the other side of the world"[40:45]
        'world'

    """
    return [m.start() for m in re.finditer(term, text)]
