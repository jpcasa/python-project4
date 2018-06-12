import sys
import datetime

from unittest.mock import patch
import unittest
from peewee import *

import engine

test_db = SqliteDatabase('test_employees.db')

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.engine = engine.Engine()
        self.entries = self.engine.get_all_entries()

    def test_init(self):
        self.engine.menu_loop('q')
        self.engine.clear()

    def test_initialize(self):
        self.engine.initialize()

    @patch('engine.input', return_value='q')
    def test_menu_loop(self, input):
        self.engine.menu_loop('1')
        self.engine.clear()

    def test_display_entry(self):
        self.engine.display_entry(self.entries[0])
        self.engine.clear()

    def test_add_simple_entry(self):
        self.engine.add_simple_entry('Juan', 'A', 10, 'Notes')
        last_entry = self.engine.get_last_entry()
        self.engine.display_entry(last_entry)
        self.engine.clear()

    @patch('engine.input', return_value='y')
    def test_delete_entry(self, input):
        self.assertEqual(self.engine.delete_entry(self.entries[0]), True)
        self.engine.clear()

    @patch('engine.input', return_value='n')
    def test_delete_entry_false(self, input):
        self.assertEqual(self.engine.delete_entry(self.entries[0]), False)
        self.engine.clear()

    def test_validate_input_string(self):
        boo = self.engine.validate_input('string', 'a')
        boo2 = self.engine.validate_input('string', 2)
        self.assertEqual(boo, True)
        self.assertEqual(boo2, False)

    def test_validate_input_int(self):
        boo = self.engine.validate_input('int', 2)
        boo2 = self.engine.validate_input('int', 'aaa')
        self.assertEqual(boo, True)
        self.assertEqual(boo2, False)

    def test_search_tasks(self):
        self.engine.add_simple_entry('Juan', 'A', 10, 'Notes')
        last = self.engine.get_last_entry()

        entries = self.engine.search_tasks('name', 'Juan')
        self.assertGreater(len(entries), 0)

        entries = self.engine.search_tasks('timestamp', datetime.date.today().strftime('%d/%m/%Y'))
        self.assertGreater(len(entries), 0)

        entries = self.engine.search_tasks('minutes', 10)
        self.assertGreater(len(entries), 0)

        entries = self.engine.search_tasks('search_term', 'Notes')
        self.assertGreater(len(entries), 0)

        self.engine.clear()

    @patch('engine.input', return_value='a')
    def test_search_entries_a(self, input):
        self.engine.search_entries()
        self.engine.clear()

    @patch('engine.input', return_value='b')
    def test_search_entries_b(self, input):
        self.engine.search_entries()
        self.engine.clear()

    @patch('engine.input', return_value='n')
    def test_view_entries(self, input):
        self.engine.view_entries()
        self.engine.clear()

    #
    # def test_view_entries(self):
    #     original_input = __builtins__.input
    #     __builtins__.input = lambda _: 'd'
    #     self.engine.view_entries()
    #     __builtins__.input = original_input
    #     self.engine.clear()


if __name__ == '__main__':
    unittest.main()
