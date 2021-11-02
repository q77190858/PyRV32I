from Memory import Memory
from Register import Register
from ControlUnit import ControlUnit
from EmulateRV32I import EmulateRV32I


def main():
    emulate = EmulateRV32I()
    # emulate.load_bin("mul_test_9_5.bin", 0x80000000, "little")
    emulate.load_bin("mul_test_ff.bin", 0x80000000, "little")
    emulate.run(0x80000000)


if __name__ == '__main__':
    main()
