# code segment
.section .text
.global _start
_start:

# emulate mul
li x1,5
li x2,9
andi x5,x1,-2048
andi x6,x2,-2048
xor x5,x5,x6
andi x1,x1,2047
andi x2,x2,2047
mv x4,x2
li x3,0
li x7,32
loop:
addi x7,x7,-1
andi x6,x4,1
beq x6,x0,shift
add x3,x3,x1
shift:
srli x3,x3,1
srli x4,x4,1
bne x7,x0,loop

print_pass:
la x10,fail_str
jal x0,print

print_fail:
la x10,pass_str

print:
li x11,0x13000000
lb x12,0(x10)
1:sb x12,0(x11)
addi x10,x10,1
lb x12,0(x10)
bne x12,x0,1b

end:
nop

# read only data segment
.section .rodata
pass_str:
.string "__pass!__\n\0"
fail_str:
.string "__fail!__\n\0"
