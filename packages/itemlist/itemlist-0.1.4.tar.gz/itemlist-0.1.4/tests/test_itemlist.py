# tests/test_itemlist.py
import unittest
from itemlist.itemlist import Item

class TestItem(unittest.TestCase):
    def setUp(self):
        self.item = Item()

    def test_add_item(self):
        def sample_func(description="Sample function"):
            pass
        self.item(sample_func)
        self.assertEqual(len(self.item.items), 1)
        self.assertEqual(self.item.items[0][0], 'sample_func')
        self.assertEqual(self.item.items[0][2], 'Sample function')

    def test_cancel_option(self):
        cancel = self.item.cancel_option
        self.assertEqual(cancel[0], "Cancel")
        self.assertEqual(cancel[2], "Cancel and exit")

if __name__ == '__main__':
    unittest.main()
