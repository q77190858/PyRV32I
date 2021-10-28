from Memory import Memory
import unittest


class TestMemory(unittest.TestCase):
    def test_memory(self):
        mem = Memory()
        mem.save_byte("0"*32, "01011010")
        with self.assertRaises(Exception):
            mem.get_byte(-24)
        with self.assertRaises(Exception):
            mem.get_byte("10")
        with self.assertRaises(Exception):
            mem.save_byte("100000000000000000000000000000000", "00110011")
        mem.save_byte("10000000000000000000000000000000", "10011011")
        self.assertEqual(mem.get_byte("0"*32), "01011010")
        self.assertEqual(mem.get_byte("1"+"0" * 31), "10011011")


if __name__ == '__main__':
    unittest.main()
