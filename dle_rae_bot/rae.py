import re
from sys import getdefaultencoding
from typing import List, Optional
from dataclasses import dataclass
import logging

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class WordDefinition:
    word: str
    description: str
    definitions: List[str]

    def __str__(self) -> str:
        definitions = '\n'.join(self.definitions)
        return f"""
{self.word}
----
{self.description}
{definitions}
        """


def get_definitions(word=None, url=None) -> Optional[WordDefinition]:
    """Search DLE RAE definitions for a given query."""
    if url is None:
        if not word or ' ' in word:
            return None
        url = 'https://dle.rae.es/%s?m=form' % word
    # Extract descriptions from html
    response = requests.get(url)
    if not response.ok:
        logging.error('failed retrieving definitions: response %s' % response)
        return None
    html = response.text
    soup = BeautifulSoup(html, 'html5lib')
    results_div = soup.find('div', attrs={'id': 'resultados'})
    if results_div is None:
        logging.debug('no definitions for word "%s"' % word)
        return None
    results_el = results_div.article
    if results_el is None:
        logging.debug('no definitions for word "%s"' % word)
        return None
    logging.debug('received article:\n%s\n' % results_el)
    if (redirect_el := results_el.find('p', class_='l2')) is not None:
        redirect_path = redirect_el.a['href']
        return get_definitions(url='https://dle.rae.es'+redirect_path)
    word_el = results_el.header
    word = get_unwrapped_content(word_el)
    description_el = results_el.find('p', class_='n2')
    description = get_unwrapped_content(description_el)
    definitions_el = results_el.find_all('p', class_='j')
    definitions = [get_unwrapped_content(d) for d in definitions_el]
    return WordDefinition(word, description=description, definitions=definitions)


def get_unwrapped_content(el: Tag) -> str:
    """Returns text context of given HTML element without internal tags."""
    if el is None:
        return ''
    for c in el.children:
        if isinstance(c, Tag):
            c.unwrap()
    return el.get_text()
