"""Module of definitions repository through HTTP requests."""
import logging
from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup

from dle_rae_bot.model import Word
from dle_rae_bot.utils import get_unwrapped_content


class DefinitionRepository(ABC):
    """Repository class for definitions."""

    @abstractmethod
    def get_definitions(self, word=None, url=None) -> Optional[Word]:
        """Search definitions for a given query."""


class HttpDefinitionRepository(DefinitionRepository):
    """Repository class for definitions through HTTP requests to RAE's DLE pages."""

    def get_definitions(self, word=None, url=None) -> Optional[Word]:
        """Search DLE RAE definitions for a given query."""
        if url is None:
            if not word or ' ' in word:
                return None
            url = 'https://dle.rae.es/%s?m=form' % word
        # Extract descriptions from html
        response = requests.get(url)
        if not response.ok:
            logging.error(
                'failed retrieving definitions: response %s', response)
            return None
        html = response.text
        soup = BeautifulSoup(html, 'html5lib')
        results_div = soup.find('div', attrs={'id': 'resultados'})
        if results_div is None:
            logging.debug('no definitions for word "%s"', word)
            return None
        results_el = results_div.article
        if results_el is None:
            logging.debug('no definitions for word "%s"', word)
            return None
        logging.debug('received article:\n%s\n', results_el)
        if (redirect_el := results_el.find('p', class_='l2')) is not None:
            redirect_path = redirect_el.a['href']
            return self.get_definitions(url='https://dle.rae.es'+redirect_path)
        word_el = results_el.header
        word = get_unwrapped_content(word_el)
        description_el = results_el.find('p', class_='n2')
        description = get_unwrapped_content(description_el)
        definitions_el = results_el.find_all('p', class_='j')
        definitions = [get_unwrapped_content(d) for d in definitions_el]
        return Word(word, description=description, definitions=definitions)
