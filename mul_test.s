#####################################################
#register:

#x1:muled number
#x2:mul number
#x3:result high
#x4:result low
#x5:overflow
#x10:loop number
#x11:tmp
#x12:tmp
#x13:check mul result low
#x14:check mul result high

#####################################################

.equ UART_BASE,0x13000000

.section .text
.global _start
_start:

	# emulate mul
	li x1,0x9          # load 2 number
	li x2,0x5

	lui x3,0           # set result high 0
	addi x4,x2,0
	
	li x10,32         # set loop time is 32
loop:
	addi x10,x10,-1   # loop-1
	lui x5,0          # set overflow 0
	
	andi x11,x4,1     # judge x4 lower bit
	beq x11,x0,shift
	add x3,x3,x1
	bleu x1,x3,shift # if result<muled or mul,overflow
	lui x5,0x80000      # overflow
shift:
	srli x4,x4,1
	slli x11,x3,31
	add x4,x11,x4
	srli x3,x3,1
	add x3,x3,x5
	bne x10,x0,loop

#print_fail:
#	la x10,fail_str
#	jal x0,print

print_pass:
	la x10,pass_str
	jal x0,print

print:
	li x11,UART_BASE
	lb x12,0(x10)
1:	sb x12,0(x11)
	addi x10,x10,1
	lb x12,0(x10)
	bne x12,x0,1b

	# char in x12
	lui x10,0x80000
0:	and x12,x10,x1
	bne x12,x0,2f
1:	lb x12,num_str
	sb x12,0(x11)
	jal x0,3f
2:	lb x12,num_str+1
	sb x12,0(x11)
3:	srli x10,x10,1
	bne x10,x0,0b

	lb x12,op_str+2
	sb x12,0(x11)
	lb x12,op_str+5
	sb x12,0(x11)

	# char in x12
	lui x10,0x80000
0:	and x12,x10,x2
	bne x12,x0,2f
1:	lb x12,num_str
	sb x12,0(x11)
	jal x0,3f
2:	lb x12,num_str+1
	sb x12,0(x11)
3:	srli x10,x10,1
	bne x10,x0,0b

	lb x12,op_str+4
	sb x12,0(x11)
	lb x12,op_str+5
	sb x12,0(x11)

	# char in x12
	lui x10,0x80000
0:	and x12,x10,x3
	bne x12,x0,2f
1:	lb x12,num_str
	sb x12,0(x11)
	jal x0,3f
2:	lb x12,num_str+1
	sb x12,0(x11)
3:	srli x10,x10,1
	bne x10,x0,0b

	# char in x12
	lui x10,0x80000
0:	and x12,x10,x4
	bne x12,x0,2f
1:	lb x12,num_str
	sb x12,0(x11)
	jal x0,3f
2:	lb x12,num_str+1
	sb x12,0(x11)
3:	srli x10,x10,1
	bne x10,x0,0b

	lb x12,op_str+5
	sb x12,0(x11)

end:
    li x3, 0x13000000
#   send CTRL+D to TUBE to indicate finish test
    addi x5, x0, 0x4
    sb x5, 0(x3)
#   dead loop
    beq x0, x0, end

.section .rodata
num_str:
	.string "01"
op_str:
	.string "+-x/=\n"
pass_str:
	.string "__pass!__\n\0"
fail_str:
	.string "__fail!__\n\0"
