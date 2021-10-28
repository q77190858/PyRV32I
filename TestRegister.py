import unittest
from Register import Register


class TestRegister(unittest.TestCase):
    def test_register(self):
        reg = Register()
        self.assertEqual(reg.get_value(), "00000000000000000000000000000000")
        with self.assertRaises(Exception):
            reg.set_value(12)
        with self.assertRaises(Exception):
            reg.set_value("0")
        with self.assertRaises(Exception):
            reg.set_value("010101")
        reg.set_value("01011010000000000000000000000001")
        self.assertEqual(reg.get_value(), "01011010000000000000000000000001")
        self.assertEqual(reg[-32:-28],"0101")


if __name__ == '__main__':
    unittest.main()
