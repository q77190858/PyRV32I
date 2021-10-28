class Register:
    """模拟寄存器类
    使用一个长度为32的字符串来保存4字节的数据
    """
    is_x0 = False

    def __init__(self):
        self.s = "0" * 32

    def __getitem__(self, index):
        if type(index)==tuple:
            return self.s[index[0]:index[1]]
        return self.s[index]

    def set_x0(self):
        self.is_x0 = True

    # 设置寄存器的值
    def set_value(self, s):
        # x0寄存器不可写
        if self.is_x0:
            return
        if type(s) != str:
            raise Exception("传入寄存器数据类型错误")
        if len(s) != 32:
            raise Exception("传入寄存器数据长度错误")
        self.s = str(s)

    # 获得寄存器的值
    # 返回16位字符串
    def get_value(self):
        return self.s

    # 打印寄存器的8位字符串
    def print(self):
        print(self.s)
