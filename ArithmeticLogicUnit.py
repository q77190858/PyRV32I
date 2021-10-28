from Register import Register


class ArithmeticLogicUnit:
    """算术逻辑单元ALU
    默认数据都为补码表示

    全加器的真值表:
    in1 | in2 | Ci-1 | Si | Ci
    0   |  0  |  0   | 0  | 0
    0   |  0  |  1   | 1  | 0
    0   |  1  |  0   | 1  | 0
    0   |  1  |  1   | 0  | 1
    1   |  0  |  0   | 1  | 0
    1   |  0  |  1   | 0  | 1
    1   |  1  |  0   | 0  | 1
    1   |  1  |  1   | 1  | 1"""
    TruthTable = [["0", "0"], ["1", "0"], ["1", "0"], ["0", "1"], ["1", "0"], ["0", "1"], ["0", "1"], ["1", "1"]]

    def __full_adder(self, in1, in2, c):
        """全加器，使用查表加速
        :param in1:第一输入，“0”或“1”的字符
        :param in2:第二输入，“0”或“1”的字符
        :param c:下级进位输入，“0”或“1”的字符
        :return:当前位结果，进位输出
        """
        input = in1 + in2 + c
        return self.TruthTable[int(input, 2)][0], self.TruthTable[int(input, 2)][1]

    def __init__(self):
        pass

    def add(self, rd, rs1, rs2):
        """32位寄存器-寄存器加法
        RISC-V硬件不处理整数运算溢出，需要软件处理
        无符号数相加溢出处理方法（假设 x6，x7 是无符号数）
        ADD x5，x6，x7
        BLTU x5，x6，overflow (跳转到 结果不正确的处理分支）
        :param rd:目的寄存器
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :return:无
        """
        sum = ["0"] * 32
        carry = "0"
        for i in range(31, -1, -1):
            sum[i], carry = self.__full_adder(rs1.get_value()[i], rs2.get_value()[i], carry)
        rd.set_value("".join(sum))

    def sub(self, rd, rs1, rs2):
        """32位寄存器-寄存器减法
        :param rd:目的寄存器
        :param rs1:被减数
        :param rs2:减数
        :return:无
        """
        revert = ["0"] * 32
        tmp = Register()
        # 将减数取反加1
        for i in range(31, -1, -1):
            if rs2.get_value()[i] == "0":
                revert[i] = "1"
            else:
                revert[i] = "0"
        tmp.set_value("".join(revert))
        self.addi(tmp, tmp, "000000000001")
        # 再相加即可
        self.add(rd, rs1, tmp)

    def addi(self, rd, rs1, imm):
        """寄存器-立即数加法
        :param rd:目的寄存器
        :param rs1:源寄存器
        :param imm: 12位二进制数字符串
        :return:无
        """
        sum = ["0"] * 32
        carry = "0"
        imm_ext = imm[0] * 20 + imm
        for i in range(31, -1, -1):
            sum[i], carry = self.__full_adder(rs1.get_value()[i], imm_ext[i], carry)
        rd.set_value("".join(sum))

    def and_(self, rd, rs1, rs2):
        """寄存器-寄存器 按位与
        :param rd: 目的寄存器
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :return:无
        """
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if rs1.get_value()[i] == "1" and rs2.get_value()[i] == "1":
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        rd.set_value("".join(tmp))

    def andi(self, rd, rs1, imm):
        """寄存器-立即数 按位与
        :param rd:目的寄存器
        :param rs1:源寄存器1
        :param imm:立即数，12位二进制字符串
        :return:无
        """
        # imm符号扩展到32位
        imm_ext = "".join(imm[0] * 20) + imm
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if rs1.get_value()[i] == "1" and imm_ext[i] == "1":
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        rd.set_value("".join(tmp))

    def or_(self, rd, rs1, rs2):
        """寄存器-寄存器 按位或
        :param rd: 目的寄存器
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :return:无
        """
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if rs1.get_value()[i] == "1" or rs2.get_value()[i] == "1":
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        rd.set_value("".join(tmp))

    def xor(self, rd, rs1, rs2):
        """寄存器-寄存器 按位异或
        :param rd: 目的寄存器
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :return:无
        """
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if rs1.get_value()[i] != rs2.get_value()[i]:
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        rd.set_value("".join(tmp))

    def ori(self, rd, rs1, imm):
        """寄存器-立即数 按位或
        :param rd:目的寄存器
        :param rs1:源寄存器1
        :param imm:立即数，12位二进制字符串
        :return:无
        """
        # imm符号扩展到32位
        imm_ext = "".join(imm[0] * 20) + imm
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if rs1.get_value()[i] == "1" or imm_ext[i] == "1":
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        rd.set_value("".join(tmp))

    def xori(self, rd, rs1, imm):
        """寄存器-立即数 按位异或
        :param rd:目的寄存器
        :param rs1:源寄存器1
        :param imm:立即数，12位二进制字符串
        :return:无
        """
        # imm符号扩展到32位
        imm_ext = "".join(imm[0] * 20) + imm
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if rs1.get_value()[i] != imm_ext[i]:
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        rd.set_value("".join(tmp))

    def sll(self, rd, rs1, rs2):
        """逻辑左移，低位补0
        :param rd:保存移位后数字
        :param rs1:需要被移位的数
        :param rs2:移位值，寄存器中低5位二进制字符串，因此最大移32位
        :return:无
        """
        rd.set_value((rs1.get_value() + "0" * int(rs2[-5:], 2))[-32:])

    def slli(self, rd, rs1, shamt):
        """立即数逻辑左移，低位补0
        :param rd:保存移位后数字
        :param rs1:需要被移位的数
        :param shamt:移位位数，5位二进制字符串，因此最大移32位
        :return:无
        """
        rd.set_value((rs1.get_value() + "0" * int(shamt, 2))[-32:])

    def srl(self, rd, rs1, rs2):
        """寄存器逻辑右移，高位补0
        :param rd:保存移位后数字
        :param rs1:需要被移位的数
        :param rs2:移位位数，寄存器低5位二进制字符串，因此最大移32位
        :return:无
        """
        rd.set_value(("0" * int(rs2[-5:], 2) + rs1.get_value())[:32])

    def srli(self, rd, rs1, shamt):
        """逻辑右移，高位补0
        :param rd:保存移位后数字
        :param rs1:需要被移位的数
        :param shamt:移位位数，5位二进制字符串，因此最大移32位
        :return:无
        """
        rd.set_value(("0" * int(shamt, 2) + rs1.get_value())[:32])

    def sra(self, rd, rs1, rs2):
        """寄存器算术右移，高位补符号位
        :param rd:保存移位后数字
        :param rs1:需要被移位的数
        :param rs2:移位位数，寄存器低5位二进制字符串，因此最大移32位
        :return:无
        """
        rd.set_value((rs1.get_value()[0] * int(rs2[-5:], 2) + rs1.get_value())[:32])

    def srai(self, rd, rs1, shamt):
        """算术右移，高位补符号位
        :param rd:保存移位后数字
        :param rs1:需要被移位的数
        :param shamt:移位位数，5位二进制字符串，因此最大移32位
        :return:无
        """
        rd.set_value((rs1.get_value()[0] * int(shamt, 2) + rs1.get_value())[:32])

    def lui(self, rd, imm):
        """载入立即数到寄存器高20位，低12位补0
        :param rd:目的寄存器
        :param imm:立即数，20位二进制字符串
        :return:无
        """
        imm_ext = imm + "0" * 12
        rd.set_value(imm_ext)

    def auipc(self, rd, pc, imm):
        """将pc的值（即当前指令的地址）加上右补12个0的立即数，存入rd
        :param rd:目的寄存器
        :param pc: 程序计数器指针
        :param imm:立即数，20位二进制字符串
        :return:无
        """
        imm_ext = imm + "0" * 12
        tmp = Register()
        tmp.set_value(imm_ext)
        self.add(rd, pc, tmp)

    def slti(self, rd, rs1, imm):
        """有符号比较 寄存器<立即数
        :param rd:真则设置为1，假为0
        :param rs1:比较寄存器，看作有符号
        :param imm:比较立即数，12位二进制字符串，看作有符号
        :return:无
        """
        # imm扩展到32位
        imm_ext = "".join(imm[0] * 20) + imm
        # 异号直接判断
        if rs1[0] == "0" and imm_ext[0] == "1":
            rd.set_value("00000000000000000000000000000000")
            return
        if rs1[0] == "1" and imm_ext[0] == "0":
            rd.set_value("00000000000000000000000000000001")
            return
        # 如果同号则相减
        # imm_ext取反加1
        tmp = ["0"] * 32
        for i in range(31, -1, -1):
            if imm_ext == "0":
                tmp[i] = "1"
            else:
                tmp[i] = "0"
        reg_tmp = Register()
        reg_tmp.set_value("".join(tmp))
        self.addi(reg_tmp, reg_tmp, "000000000001")
        self.add(reg_tmp, rs1, reg_tmp)
        if reg_tmp.get_value()[0] == "1":
            rd.set_value("00000000000000000000000000000001")
        else:
            rd.set_value("00000000000000000000000000000000")

    def sltiu(self, rd, rs1, imm):
        """无符号比较 寄存器<立即数
        :param rd:真则设置为1，假为0
        :param rs1:比较寄存器
        :param imm:比较立即数，12位二进制字符串
        :return:无
        """
        # imm符号扩展到32位，再当做无符号数处理
        imm_ext = "".join(imm[0] * 20) + imm
        tmp = Register()
        tmp.set_value(imm_ext)
        self.sub(tmp, rs1, tmp)
        if tmp[0] == "1":
            rd.set_value("00000000000000000000000000000001")
        else:
            rd.set_value("00000000000000000000000000000000")

    def slt(self, rd, rs1, rs2):
        """寄存器rs1 < 寄存器rs2 有符号数比较
        :param rd:目的寄存器，小于为1，否则为0
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :return:无
        """
        if rs1[0] == "0" and rs2[0] == "1":
            rd.set_value("00000000000000000000000000000000")
            return
        if rs1[0] == "1" and rs2[0] == "0":
            rd.set_value("00000000000000000000000000000001")
            return
        tmp = Register()
        self.sub(tmp, rs1, rs2)
        if tmp[0] == "1":
            rd.set_value("00000000000000000000000000000001")
        else:
            rd.set_value("00000000000000000000000000000000")

    def sltu(self, rd, rs1, rs2):
        """寄存器rs1 < 寄存器rs2 无符号数比较
        :param rd:目的寄存器，小于为1，否则为0
        :param rs1:源寄存器1
        :param rs2:源寄存器2
        :return:无
        """
        tmp = Register()
        self.sub(tmp, rs1, rs2)
        if tmp.get_value()[0] == "1":
            rd.set_value("00000000000000000000000000000001")
        else:
            rd.set_value("00000000000000000000000000000000")
