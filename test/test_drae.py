import unittest

from bs4 import BeautifulSoup
from dle_rae_bot.model import WordDefinition
from dle_rae_bot.repository import HttpDefinitionRepository
from dle_rae_bot.utils import get_unwrapped_content


class TestGetDefinitions(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.repository = HttpDefinitionRepository()

    def test_when_empty_word_then_none_result(self):
        self.assertIsNone(self.repository.get_definitions())

    def test_when_word_with_spaces_then_none_result(self):
        self.assertIsNone(self.repository.get_definitions())

    def test_when_unknown_then_none_result(self):
        self.assertIsNone(self.repository.get_definitions())

    def test_when_word_then_word_definition_result(self):
        expected = WordDefinition(
            word='diccionario',
            description='Del b. lat. dictionarium.',
            definitions=[
                '1. m. Repertorio en forma de libro o en soporte electrónico en el que se recogen, según un orden determinado, las palabras o expresiones de una o más lenguas, o de una materia concreta, acompañadas de su definición, equivalencia o explicación.',
                '2. m. Catálogo de noticias o datos de un mismo género, ordenado alfabéticamente. Diccionario bibliográfico, biográfico, geográfico.'
            ]
        )
        actual = self.repository.get_definitions('diccionario')
        self.assertEquals(expected, actual)

    def test_when_word_has_redirect_then_word_definition_result(self):
        expected = WordDefinition(
            word='jefe, fa',
            description='Del fr. chef.',
            definitions=[
                '1. m. y f. Superior o cabeza de una corporación, partido u oficio.',
                '2. m. y f. Mil. Militar con cualquiera de los grados de comandante, teniente coronel y coronel en el Ejército, o los de capitán de corbeta, capitán de fragata y capitán de navío en la Armada.',
            ]
        )
        actual = self.repository.get_definitions('jefa')
        self.assertEquals(expected, actual)


class TestGetUnwrappedContent(unittest.TestCase):

    def test_when_empty_element_then_empty_text(self):
        self.assertEqual(get_unwrapped_content(None), '')

    def test_when_element_without_tags_then_element_text(self):
        el = BeautifulSoup('<p>text</p>', 'html5lib')
        self.assertEqual(get_unwrapped_content(el), 'text')

    def test_when_element_with_tags_then_element_text_without_tags(self):
        el = BeautifulSoup('<p>text <b>bold text</b></p>', 'html5lib')
        self.assertEqual(get_unwrapped_content(el), 'text bold text')


if __name__ == '__main__':
    unittest.main()
