from Register import Register
from ArithmeticLogicUnit import ArithmeticLogicUnit
import unittest


class TestArithmeticLogicUnit(unittest.TestCase):
    def test_add(self):
        rd = Register()
        rs1 = Register()
        rs2 = Register()
        alu = ArithmeticLogicUnit()
        rs1.set_value("10000001000000011001100000000001")
        rs2.set_value("01100001000000011000000110000001")
        alu.add(rd, rs1, rs2)
        self.assertEqual(rd.get_value(), "11100010000000110001100110000010")
        rs1.set_value("00000000000000000000000000000001")
        rs2.set_value("11111111111111111111111111111111")
        alu.add(rd, rs1, rs2)
        self.assertEqual(rd.get_value(), "00000000000000000000000000000000")

    def test_addi(self):
        rd = Register()
        rs1 = Register()
        alu = ArithmeticLogicUnit()
        rs1.set_value("10000001000000011001100000000001")
        alu.addi(rd, rs1, "000000000000")
        self.assertEqual(rd.get_value(), "10000001000000011001100000000001")
        alu.addi(rd, rs1, "010110101111")
        self.assertEqual(rd.get_value(), "10000001000000011001110110110000")

    def test_sub(self):
        rd = Register()
        rs1 = Register()
        rs2 = Register()
        alu = ArithmeticLogicUnit()
        rs1.set_value("10000001000000011001100000000001")
        rs2.set_value("01100001000000011000000110000001")
        alu.sub(rd, rs1, rs2)
        self.assertEqual(rd.get_value(), "00100000000000000001011010000000")
        rs1.set_value("00000000000000000000000000000001")
        rs2.set_value("11111111111111111111111111111111")
        alu.sub(rd, rs1, rs2)
        self.assertEqual(rd.get_value(), "00000000000000000000000000000010")

    def test_slli(self):
        rd = Register()
        rs1 = Register()
        alu = ArithmeticLogicUnit()
        rs1.set_value("00001111111111111111111111111111")
        alu.slli(rd, rs1, "00010")
        self.assertEqual(rd.get_value(), "00111111111111111111111111111100")
        alu.slli(rd, rd, "00100")
        self.assertEqual(rd.get_value(), "11111111111111111111111111000000")

    def test_sltu(self):
        rd = Register()
        rs1 = Register()
        rs2 = Register()
        alu = ArithmeticLogicUnit()
        rs1.set_value('01111111111111111111111111111110')
        rs2.set_value('11111111111111111111111111111111')
        alu.sltu(rd, rs1, rs2)
        self.assertEqual(rd.get_value(), "00000000000000000000000000000001")

if __name__ == '__main__':
    unittest.main()
