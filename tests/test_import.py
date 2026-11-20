"""Check the word-list import callback with and without a selected file."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from activity import Sindiente


class ImportTest(unittest.TestCase):
    def setUp(self):
        self.chooser = Mock()
        self.chooser.get_uri.return_value = None
        self.target = SimpleNamespace(archivo=self.chooser, combo=Mock(),
                                      nivel=4, sugar_data='/unused/')

    def test_no_selection_does_not_import_or_change_level(self):
        with patch('activity.utils.importar_lista_p') as importer:
            Sindiente._importar_archivo_cb(self.target, None)
        importer.assert_not_called()
        self.target.combo.get_active.assert_not_called()
        self.assertEqual(self.target.nivel, 4)

    def test_selected_file_and_category_are_passed_to_importer(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / 'words.palabra'
            filename.write_text('hola:saludo:pista\n')
            self.chooser.get_uri.return_value = filename.as_uri()
            self.target.combo.get_active.return_value = 7
            with patch('activity.utils.importar_lista_p') as importer:
                Sindiente._importar_archivo_cb(self.target, None)
            importer.assert_called_once_with('/unused/', str(filename), 7)

    def test_selected_word_list_is_written_to_custom_category(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / 'words.palabra'
            content = 'Prueba\nsol:estrella:luz\n'
            filename.write_text(content)
            self.chooser.get_uri.return_value = filename.as_uri()
            self.target.sugar_data = directory + '/'
            self.target.combo.get_active.return_value = 7
            Sindiente._importar_archivo_cb(self.target, None)
            self.assertEqual((Path(directory) / 'nivel8.palabra').read_text(),
                             content)


if __name__ == '__main__':
    unittest.main()
