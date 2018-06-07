import sys

import unittest
from mock import patch

import engine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.engine = engine.Engine()
        self.entries = self.engine.get_all_entries()

    def test_add(self):
        self.assertEqual(3, 3)

    def test_init(self):
        self.engine.menu_loop('q')

    def test_display_entry(self):
        self.engine.display_entry(self.entries[0])

    def test_add_simple_entry(self):
        self.engine.add_simple_entry('Juan', 'A', 10, 'Notes')
        last_entry = self.engine.get_last_entry()
        self.engine.display_entry(last_entry)

    def test_delete_entry(self):
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: 'y'
        self.assertEqual(self.engine.delete_entry(self.entries[0]), True)
        __builtins__.raw_input = original_raw_input

    def test_delete_entry_false(self):
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: 'n'
        self.assertEqual(self.engine.delete_entry(self.entries[0]), False)
        __builtins__.raw_input = original_raw_input

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



if __name__ == '__main__':
    unittest.main()
