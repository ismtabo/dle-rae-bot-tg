"""Module for html utilities."""

from bs4 import Tag


def get_unwrapped_content(tag: Tag) -> str:
    """Returns text context of given HTML element without internal tags."""
    if tag is None:
        return ''
    for child in tag.children:
        if isinstance(child, Tag):
            child.unwrap()
    return tag.get_text()
