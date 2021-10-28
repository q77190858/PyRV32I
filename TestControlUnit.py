from ControlUnit import ControlUnit
from ArithmeticLogicUnit import ArithmeticLogicUnit
from Memory import Memory
from Register import Register
import unittest


class TestControlUnit(unittest.TestCase):
    mem = Memory()
    regs = []
    for i in range(32):
        regs.append(Register())
    regs[0].set_x0()
    cu = ControlUnit(mem, regs)

    def test_lb(self):
        self.regs[1].set_value("1" + "0" * 30 + "1")
        self.mem.save_byte(self.regs[1].get_value(), "11110000")
        self.cu.lb(self.regs[3], self.regs[1], "000000000000")
        self.assertEqual(self.regs[3].get_value()[-8:], "11110000")

    def test_sh(self):
        self.regs[1].set_value("0"*16+"1010110010010011")
        self.cu.sh(self.regs[0],self.regs[1],"000000000000")
        self.assertEqual(self.mem.get_byte("0"*32),"10101100")
        self.assertEqual(self.mem.get_byte("0" * 31+"1"), "10010011")

    def test_instruct_decode(self):
        pass


if __name__ == '__main__':
    unittest.main()
