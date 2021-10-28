# PyRV32I 模拟器

RISC-V RV32I指令集模拟器(Python实现)

## 特点：

1. 使用python模拟实现`risc-v rv32i`指令集

2. 32位地址空间，动态分配内存
3. x0-x31 共32个寄存器
4. 可直接运行由`riscv32-unknown-linux-gnu-gcc`编译出的bin文件
5. 支持大端(big-endian)、小端(little-endia)模式
6. 模拟五级流水线`IF`->`ID`->`EX`->`MEM`->`WB`
7. 模拟`UART`映射到0x13000000内存，支持串口输出
8. 目前只有m态

## 指令实现：

| **分类**       | **指令**                                                     | **数目** |        |
| -------------- | :----------------------------------------------------------- | -------- | ------ |
| 算术和逻辑运算 | LUI/AUIPC<br />ADDI/SLTI/SLTIU/ADD/SUB/SLT/SLTU<br />SLLI/SRLI/SRAI/SLL/SRL/SRA<br />ANDI/ORI/XORI/AND/OR/XOR | 21       | 实现   |
| 控制           | JAL/JALR<br />BEQ/BNE/BLT/BGE/BLTU/BGEU                      | 8        | 实现   |
| 数据传输       | LB/LH/LW/LBU/LHU<br />SB/SH/SW                               | 8        | 实现   |
| 其他           | FENCE/ECALL/EBREAK                                           | 3        | 待实现 |
| 总计           | 40                                                           |          |        |

## 交叉编译方法：

```shell
# mul.s -> mul.o
riscv32-unknown-linux-gnu-gcc -nostdlib -c -o mul.o mul.s
# mul.o -> mul.elf
riscv32-unknown-linux-gnu-ld -nostdlib -Ttext=0x80000000 -o mul.elf mul.o
# mul.elf -> mul.dis
riscv32-unknown-linux-gnu-objdump -D mul.elf > mul.dis
# mul.elf -> mul.bin
riscv32-unknown-linux-gnu-objcopy -O binary mul.elf mul.bin
```

## 待增加特性：

1. 运行汇编指令文件
2. 运行文本格式字节码文件
3. 实现`ECALL`/`EBREAK`指令
4. 实现`CSR`指令、`CSR`寄存器、异常中断处理、3种特权态和切换