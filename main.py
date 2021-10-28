from Memory import Memory
from Register import Register
from ControlUnit import ControlUnit
from EmulateRV32I import EmulateRV32I


def main():
    emulate = EmulateRV32I()
    emulate.load_bin("hello.bin", 0x80000000, "little")
    emulate.run(0x80000000)
    print("".join(emulate.mem.uart))


if __name__ == '__main__':
    main()
