from dataclasses import dataclass
from typing import List


@dataclass
class WordDefinition:
    word: str
    description: str
    definitions: List[str]

    def markdown(self) -> str:
        definitions = '\n'.join(self.definitions)
        return f"""
*{self.word}*
_{self.description}_
{definitions}
        """
