"""Model of definition model."""

from dataclasses import dataclass
from typing import List


@dataclass
class Word:
    """WordDefinition represents a DLE RAE's word with description and definitions."""
    word: str
    description: str
    definitions: List[str]

    def markdown(self) -> str:
        """Returns string Markdown representation of the word"""
        definitions = '\n'.join(self.definitions)
        return f"""
*{self.word}*
_{self.description}_
{definitions}
        """
