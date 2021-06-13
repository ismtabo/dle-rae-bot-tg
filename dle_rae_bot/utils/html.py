from bs4 import Tag


def get_unwrapped_content(el: Tag) -> str:
    """Returns text context of given HTML element without internal tags."""
    if el is None:
        return ''
    for c in el.children:
        if isinstance(c, Tag):
            c.unwrap()
    return el.get_text()
