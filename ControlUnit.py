from Register import Register
from Memory import Memory
from ArithmeticLogicUnit import ArithmeticLogicUnit


class ControlUnit:
    # 定义alu
    alu = ArithmeticLogicUnit()
    # 指令寄存器
    ir = Register()
    # 程序计数器
    pc = Register()
    # 程序计数器的旧值
    old_pc = Register()
    # 默认字节序
    endian = "big"

    # 保存译码中间变量
    # 指令类型
    instruction_type = "r-type"
    # 操作码7位
    opcode = "0000000"
    # funct3 3位
    funct3 = "000"
    # funct7 7位
    funct7 = "0000000"
    rd_id = 0
    rs1_id = 0
    rs2_id = 0
    # 一般的12位立即数
    imm12 = "000000000000"
    # 用于 U-type 的20位长立即数
    imm20 = "00000000000000000000"
    # 用于移位的5位 短立即数
    shamt = "00000"

    def __init__(self, mem, regs, endian):
        # 定义内存
        self.mem = mem
        # 定义x0-x31寄存器，其中x0永远为0
        self.x = regs
        # 设置big little 大小端
        self.endian = endian

    def lb(self, rd, rs1, imm):
        """载入一个字节byte，按有符号扩展
        :param rd:目的寄存器
        :param rs1:内存基址寄存器1
        :param imm:内存偏移地址，有符号12位字符串
        :return:无
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)
        byte = self.mem.get_byte(tmp.get_value())
        rd.set_value(byte[0] * 24 + byte)

    def lbu(self, rd, rs1, imm):
        """载入一个字节byte，按无符号扩展到32位
        :param rd:目的寄存器
        :param rs1:内存基址寄存器1
        :param imm:内存偏移地址，有符号12位字符串
        :return:无
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)
        byte = self.mem.get_byte(tmp.get_value())
        rd.set_value("0" * 24 + byte)

    def lh(self, rd, rs1, imm):
        """载入一个半字half word，按有符号扩展
        :param rd:目的寄存器
        :param rs1:内存基址寄存器1
        :param imm:内存偏移地址，有符号12位字符串
        :return:无
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)
        byte1 = self.mem.get_byte(tmp.get_value())
        self.alu.addi(tmp, tmp, "000000000001")
        byte2 = self.mem.get_byte(tmp.get_value())
        # 大端字节序
        if self.endian=="big":
            rd.set_value(byte1[0] * 16 + byte1 + byte2)
        # 小端字节序
        elif self.endian=="little":
            rd.set_value(byte1[0] * 16 + byte2 + byte1)
    def lhu(self, rd, rs1, imm):
        """载入一个半字half word，按无符号扩展
        :param rd:目的寄存器
        :param rs1:内存基址寄存器1
        :param imm:内存偏移地址，有符号12位字符串
        :return:无
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)

        byte1 = self.mem.get_byte(tmp.get_value())
        self.alu.addi(tmp, tmp, "000000000001")
        byte2 = self.mem.get_byte(tmp.get_value())
        # 大端字节序
        if self.endian == "big":
            rd.set_value("0" * 16 + byte1 + byte2)
        # 小端字节序
        elif self.endian == "little":
            rd.set_value("0" * 16 + byte2 + byte1)

    def lw(self, rd, rs1, imm):
        """载入一个字word，不需要扩展
        :param rd:目的寄存器
        :param rs1:内存基址寄存器1
        :param imm:内存偏移地址，有符号12位01字符串
        :return:无
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)

        byte1 = self.mem.get_byte(tmp.get_value())
        self.alu.addi(tmp, tmp, "000000000001")
        byte2 = self.mem.get_byte(tmp.get_value())
        self.alu.addi(tmp, tmp, "000000000001")
        byte3 = self.mem.get_byte(tmp.get_value())
        self.alu.addi(tmp, tmp, "000000000001")
        byte4 = self.mem.get_byte(tmp.get_value())
        # 大端字节序
        if self.endian == "big":
            rd.set_value(byte1 + byte2 + byte3 + byte4)
        # 小端字节序
        elif self.endian == "little":
            rd.set_value(byte4 + byte3 + byte2 + byte1)

    def sb(self, rs1, rs2, imm):
        """保存1个byte
        :param rs1:内存基址寄存器
        :param rs2:需要保存的内容在低8位
        :param imm:内存偏移地址，有符号12位01字符串
        :return:
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)
        self.mem.save_byte(tmp.get_value(), rs2.get_value()[-8:])

    def sh(self, rs1, rs2, imm):
        """保存1个半字half word
        :param rs1:内存基址寄存器
        :param rs2:需要保存的内容在低16位
        :param imm:内存偏移地址，有符号12位01字符串
        :return:
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)
        # 大端字节序
        if self.endian == "big":
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[-16:-8])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[-8:])
        # 小端字节序
        elif self.endian == "little":
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[-8:])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[-16:-8])


    def sw(self, rs1, rs2, imm):
        """保存1个字 word
        :param rs1:内存基址寄存器
        :param rs2:需要保存的32位数据
        :param imm:内存偏移地址，有符号12位01字符串
        :return:
        """
        tmp = Register()
        tmp.set_value(imm[0] * 20 + imm)
        self.alu.add(tmp, rs1, tmp)
        # 大端字节序
        if self.endian == "big":
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[:8])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[8:16])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[16:24])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[24:])
        # 小端字节序
        elif self.endian == "little":
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[24:])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[16:24])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[8:16])
            self.alu.addi(tmp, tmp, "000000000001")
            self.mem.save_byte(tmp.get_value(), rs2.get_value()[:8])

    def beq(self, rs1, rs2, imm):
        """相等则跳转到imm对应的偏移量
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        for i in range(31, -1, -1):
            if rs1.get_value()[i] != rs2.get_value()[i]:
                return
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def bne(self, rs1, rs2, imm):
        """不等则跳转到imm对应的偏移量
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        is_equal=True
        for i in range(31, -1, -1):
            if rs1.get_value()[i] != rs2.get_value()[i]:
                is_equal=False
                break
        if is_equal:
            return
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def blt(self, rs1, rs2, imm):
        """rs1<rs2 则跳转到imm对应的偏移量
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        tmp = Register()
        self.alu.slt(tmp, rs1, rs2)
        if tmp.get_value()[0] != "00000000000000000000000000000001":
            return
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def bge(self, rs1, rs2, imm):
        """rs1>=rs2 则跳转到imm对应的偏移量
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        tmp = Register()
        self.alu.slt(tmp, rs1, rs2)
        if tmp.get_value()[0] == "00000000000000000000000000000001":
            return
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def bltu(self, rs1, rs2, imm):
        """rs1<rs2 看作无符号数 则跳转到imm对应的偏移量
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        tmp = Register()
        self.alu.sltu(tmp, rs1, rs2)
        if tmp.get_value()[0] != "00000000000000000000000000000001":
            return
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def bgeu(self, rs1, rs2, imm):
        """rs1>=rs2 看作无符号数 则跳转到imm对应的偏移量
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        tmp = Register()
        self.alu.sltu(tmp, rs1, rs2)
        if tmp.get_value()[0] == "00000000000000000000000000000001":
            return
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def jal(self, rd, imm):
        """跳转并链接
        :param rd:保存原pc+4到rd
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        self.alu.addi(rd, self.pc, "000000000100")
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, self.pc, offset)

    def jalr(self, rd, rs1, imm):
        """跳转并链接寄存器
        :param rd:保存原pc+4到rd
         :param rs1:基址寄存器
        :param imm:有符号偏移量，单位为2byte，12位01字符串
        :return:无
        """
        self.alu.add(rd, self.pc, "000000000100")
        offset = Register()
        offset.set_value(imm[0] * 20 + imm)
        self.alu.add(offset, offset, offset)
        self.alu.add(self.pc, rs1, offset)

    def fence(self):
        """由于目前是单hart模型，所以不用实现访存维序
        :return:无
        """
        pass

    def hint(self):
        """用于微架构性能计数器，不实现
        :return:
        """
        pass

    def ecall(self):
        pass

    def ebreak(self):
        pass

    def instruction_fetch(self):
        """取指
        :return: 无
        """
        self.lw(self.ir, self.pc, "000000000000")
        print("{0} : {1}  ".format(self.pc.get_value(),self.ir.get_value()),end="")
        # 保存一个旧pc副本，方便判断pc是否有修改
        self.old_pc.set_value(self.pc.get_value())

    def instruction_decode(self):
        """译码，根据指令type提取出操作码和操作数
        :return: 无
        """
        self.opcode = self.ir[-7:]
        # r-type
        if self.opcode == "0110011":
            self.instruction_type = "r-type"
            self.rd_id = int(self.ir[-12:-7], 2)
            self.funct3 = self.ir[-15:-12]
            self.rs1_id = int(self.ir[-20:-15], 2)
            self.rs2_id = int(self.ir[-25:-20], 2)
            self.funct7 = self.ir[-32:-25]
        # lui和auipc
        elif self.opcode == "0110111" or self.opcode == "0010111":
            self.instruction_type = "u-type"
            self.rd_id = int(self.ir[-12, -7], 2)
            self.imm20 = self.ir[-32:-12]
        # jal
        elif self.opcode == "1101111":
            self.instruction_type = "j-type"
            self.rd_id = int(self.ir[-12, -7], 2)
            self.imm20 = self.ir[-32:-12][-21:-20] + self.ir[-32:-12][-9:] + self.ir[-32:-12][-10:-9] + self.ir[
                                                                                                        -32:-12][
                                                                                                        -20:-10]
        # jalr
        elif self.opcode == "1100111":
            self.instruction_type = "i-type"
            self.rd_id = int(self.ir[-12, -7], 2)
            self.funct3 = self.ir[-15:-12]
            self.rs1_id = int(self.ir[-20, -15], 2)
            self.imm12 = self.ir[-32:-20]
        # b-type
        elif self.opcode == "1100011":
            self.instruction_type = "b-type"
            self.imm12 = self.ir[-32:-31] + self.ir[-8:-7] + self.ir[-31:-25] + self.ir[-12:-8]
            self.funct3 = self.ir[-15:-12]
            self.rs1_id = int(self.ir[-20, -15], 2)
            self.rs2_id = int(self.ir[-25, -20], 2)
        # i-type load
        elif self.opcode == "0000011":
            self.instruction_type = "i-type"
            self.rd_id = int(self.ir[-12, -7], 2)
            self.funct3 = self.ir[-15:-12]
            self.rs1_id = int(self.ir[-20, -15], 2)
            self.imm12 = self.ir[-32:-20]
        # s-type store
        elif self.opcode == "0100011":
            self.instruction_type = "s-type"
            self.imm12 = self.ir[-32:-25] + self.ir[-12:-7]
            self.funct3 = self.ir[-15:-12]
            self.rs1_id = int(self.ir[-20, -15], 2)
            self.rs2_id = int(self.ir[-25, -20], 2)
        # i-type addi compare bit_op
        elif self.opcode == "0010011":
            self.instruction_type = "i-type"
            self.rd_id = int(self.ir[-12, -7], 2)
            self.funct3 = self.ir[-15:-12]
            self.rs1_id = int(self.ir[-20, -15], 2)
            self.imm12 = self.ir[-32:-20]
            if self.funct3 == "001" or self.funct3 == "101":
                self.shamt = self.imm12[-5:]
                self.funct7 = self.imm12[-12:-5]
        # i-type fence
        elif self.opcode == "0000111":
            self.instruction_type = "i-type"
        # i-type ecall ebreak and csr
        elif self.opcode == "1110011":
            self.instruction_type = "i-type"
            self.rd_id = int(self.ir[-12:-7], 2)
            self.funct3 = self.ir[-15:-12]

    def exe(self):
        """执行所有alu操作
        :return:无
        """
        if self.opcode == "0110111":
            print("lui x{0}, {1}".format(self.rd_id, self.imm20))
            self.alu.lui(self.x[self.rd_id], self.imm20)
        elif self.opcode == "0010111":
            print("auipc x{0}, {1}".format(self.rd_id, self.imm20))
            self.alu.auipc(self.x[self.rd_id], self.pc, self.imm20)
        elif self.opcode == "0010011":
            if self.funct3 == "000":
                print("addi x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id,self.imm12))
                self.alu.addi(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "010":
                print("slti x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.alu.slti(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "011":
                print("sltiu x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.alu.sltiu(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "100":
                print("xori x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.alu.xori(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "110":
                print("ori x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.alu.ori(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "111":
                print("andi x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.alu.andi(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "001":
                print("slli x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.shamt))
                self.alu.slli(self.x[self.rd_id], self.x[self.rs1_id], self.shamt)
            elif self.funct3 == "101":
                if self.funct7 == "0000000":
                    print("srli x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.shamt))
                    self.alu.srli(self.x[self.rd_id], self.x[self.rs1_id], self.shamt)
                elif self.funct7 == "0100000":
                    print("srai x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.shamt))
                    self.alu.srai(self.x[self.rd_id], self.x[self.rs1_id], self.shamt)
        elif self.opcode == "0110011":
            if self.funct3 == "000":
                if self.funct7 == "0000000":
                    print("add x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                    self.alu.add(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
                elif self.funct7 == "0100000":
                    print("sub x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                    self.alu.sub(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "001":
                print("sll x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                self.alu.sll(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "010":
                print("slt x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                self.alu.slt(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "011":
                print("sltu x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                self.alu.sltu(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "100":
                print("xor x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                self.alu.xor(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "101":
                if self.funct7 == "0000000":
                    print("srl x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                    self.alu.srl(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
                elif self.funct7 == "0100000":
                    print("sra x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                    self.alu.sra(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "110":
                print("or x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                self.alu.or_(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])
            elif self.funct3 == "111":
                print("and x{0}, x{1}, x{2}".format(self.rd_id, self.rs1_id, self.rs2_id))
                self.alu.and_(self.x[self.rd_id], self.x[self.rs1_id], self.x[self.rs2_id])

    def mem_access(self):
        """执行load操作
        :return:无
        """
        if self.opcode == "1101111":
            print("jal x{0}, {1}".format(self.rd_id, self.imm12))
            self.jal(self.x[self.rd_id], self.imm12)
        elif self.opcode == "1100111":
            print("jalr x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
            self.jalr(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
        elif self.opcode == "1100011":
            if self.funct3 == "000":
                print("beq x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.beq(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "001":
                print("bne x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.bne(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "100":
                print("blt x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.blt(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "101":
                print("bge x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.bge(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "110":
                print("bltu x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.bltu(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "111":
                print("bgeu x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.bgeu(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
        elif self.opcode == "0000011":
            if self.funct3 == "000":
                print("lb x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.lb(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "001":
                print("lh x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.lh(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "010":
                print("lw x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.lw(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "100":
                print("lbu x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.lbu(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
            elif self.funct3 == "101":
                print("lhu x{0}, x{1}, {2}".format(self.rd_id, self.rs1_id, self.imm12))
                self.lhu(self.x[self.rd_id], self.x[self.rs1_id], self.imm12)
        elif self.opcode == "0001111":
            print("fence")
            self.fence()
        elif self.opcode == "1110011":
            if self.funct3 == "000":
                if self.funct7 == "0000000":
                    print("ecall")
                    self.ecall()
                elif self.funct7 == "0000001":
                    print("ebreak")
                    self.ebreak()

    def write_back(self):
        """执行store操作
        :return:无
        """
        if self.opcode == "0100011":
            if self.funct3 == "000":
                print("sb x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.sb(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "001":
                print("sh x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.sh(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
            elif self.funct3 == "010":
                print("sw x{0}, x{1}, {2}".format(self.rs1_id, self.rs2_id, self.imm12))
                self.sw(self.x[self.rs1_id], self.x[self.rs2_id], self.imm12)
        # pc指向下一条指令地址
        if self.pc.get_value() == self.old_pc.get_value():
            self.alu.addi(self.pc, self.pc, "000000000100")
