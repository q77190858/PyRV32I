# code segment
.section .text
.global _start
_start:

la x10,hello_str
li x11,0x13000000
lb x12,0(x10)
1:sb x12,0(x11)
addi x10,x10,1
lb x12,0(x10)
bne x12,x0,1b

# read only data segment
.section .rodata
hello_str:
.string "__hello world!__\n\0"
