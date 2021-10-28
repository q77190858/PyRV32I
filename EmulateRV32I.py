from Memory import Memory
from Register import Register
from ControlUnit import ControlUnit
import os


class EmulateRV32I:
    """
    RISV-V RV32I基本整数指令集模拟器
    定义0x13000000地址为串口发送数据寄存器
    """

    def __init__(self):
        self.endian = "big"
        self.mem = Memory()
        self.regs = []
        for i in range(32):
            self.regs.append(Register())
        self.regs[0].set_x0()
        self.cu = ControlUnit(self.mem, self.regs, self.endian)

    def load_bin(self, bin_file, base_addr, endian):
        """载入bin裸板文件
        :param bin_file:bin裸板文件路径
        :param base_addr:载入内存的起始地址，十六进制整数
        :param endian: big or little 大端或者小端字节序
        :return:无
        """
        self.endian = endian
        self.cu.endian = endian
        bytecode = []
        with open(bin_file, "rb") as file:
            for i in range(os.path.getsize(bin_file)):
                byte = file.read(1)
                byte_str = bin(int(byte.hex(), 16))[2:]
                byte_str = ("00000000" + byte_str)[-8:]
                bytecode.append(byte_str)
        for i in range(len(bytecode)):
            addr = ("0" * 32 + bin(int(str(base_addr + i), 10))[2:])[-32:]
            self.mem.save_byte(addr, bytecode[i])
        # self.mem.print()

    def load_bytecode(self, bytecode_file, endian):
        """载入字节码文本文件
        :param bytecode_file:字节码文本文件
        :param endian:big or little 大端或者小端字节序
        :return:无
        """
        pass

    def run(self, base_addr):
        """模拟器运行
        :param base_addr: 运行的起始地址，十六进制整数
        :return: 无
        """
        base_addr_str = ("0" * 32 + bin(base_addr)[2:])[-32:]
        self.cu.pc.set_value(base_addr_str)
        for i in range(66):
            self.cu.instruction_fetch()
            self.cu.instruction_decode()
            self.cu.exe()
            self.cu.mem_access()
            self.cu.write_back()

        # while True:
        #     # 5级流水线
        #     self.cu.instruction_fetch()
        #     self.cu.instruction_decode()
        #     self.cu.exe()
        #     self.cu.mem_access()
        #     self.cu.write_back()
