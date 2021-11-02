import sys


class Memory:
    """模拟内存类
    使用一个长度为8的字符串来保存1字节的数据
    地址采用32位01字符串编码
    最大支持2^32字节（4G）的数据，使用字典来动态分配内存
    """

    def __init__(self):
        self.addr_range = pow(2, 32)
        self.dic = {}
        self.uart=[]

    def get_byte(self, addr):
        """从内存读取一个字节
        :param addr:读取地址，32位01字符串
        :return:8位01字符串
        """
        if type(addr) != str or len(addr)!=32:
            raise Exception("读地址类型错误",type(addr))
            return
        # 地址越界异常
        if int(addr,2) < 0 or int(addr,2) >= self.addr_range:
            raise Exception("读地址越界", addr)
            return
        # 地址不在字典中，认为未初始化的地址，返回0
        if addr not in self.dic:
            return "00000000"
        # 否则返回地址对应的byte
        return self.dic[addr]

    def save_byte(self, addr, value):
        """向内存保存一个字节
        :param addr:写地址，32位01字符串
        :param value:8位01字符串
        :return:无
        """
        if type(addr) != str or len(addr)!=32:
            raise Exception("写地址类型错误",type(addr))
            return
        # 地址越界抛出异常
        if int(addr,2) < 0 or int(addr,2) >= self.addr_range:
            raise Exception("写地址越界", addr, value)
            return
        if type(value) != str or len(value)!=8 or int(value,2) < 0 or int(value,2) >= 256:
            raise Exception("数据类型错误",type(addr))
            return
        # 如果地址是0x13000000,则将数据写入串口
        if addr=="00010011000000000000000000000000":
            # 如果数据等于4，则程序退出
            if value=="00000100":
                sys.exit()
            self.uart.append(chr(int(value,2)))
            print(chr(int(value,2)),end="")
        # 否则将值存入字典
        else:
            self.dic[addr] = value

    # 输出内存所有信息
    def print(self):
        for k in self.dic:
            print(str(k) + ": " + self.dic[k] + " , ", end="")
        print("")