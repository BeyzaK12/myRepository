.data
#example input  
values:  .word 13, 16, 16, 7, 7 #array contents
size:    .word 5 		#size of the array

noSecond:.asciiz	"\nNo second smallest.\n"
string:  .asciiz	"The second smallest is: "

# Your code will be tested with various inputs
.text
#write your code below

la $s0, values		# values' address
lw $s1, size		# size of the array
addi $s1,$s1,-1

#   small in s3
#   secsmall in s4

loop1:
#dual comparison

	bge $t0,$s1, loop2	# i in t0
	
	sll $t4,$t0,2		#to increase address
	add $t7,$t4,$s0
	lw $t2,($t7)		# values[i] = t2
	lw $t3,4($t7)		# values[i+1] = t3
	
	
	blt $t2,$t3,if1		# t2 < t3
	bgt $t2,$t3,elseif1	# t2 > t3
	beq $t2,$t3,else1	# t2 = t3
	
	if1:
		add $s3,$0,$t2
		add $s4,$0,$t3
		
		addi $t0,$t0,1
		j loop1

	elseif1:
		add $s3,$0,$t3
		add $s4,$0,$t2
		
		addi $t0,$t0,1
		j loop1
		
	else1:
		add $s3,$0,$t2
		
		addi $t0,$t0,1
		j loop1

loop2:
#comparison 1-1

	beq $t1,$s1,x		#if comparison is done
	
	sll $t0,$t1,2		#to increase address
	add $t6,$t0,$s0
	lw $t2,($t6)		# values[k] = t2
	
	blt $s3,$t2,if2
	bgt $s3,$t2,elseif2
	beq $s3,$t2,else2
	
	if2:
		blt $t2,$s4,ccc
		
		addi $t1,$t1,1
		j loop2
		ccc:
			add $s4,$0,$t2
			
			addi $t1,$t1,1
			j loop2
	
	elseif2:
		add $s4,$0,$s3
		add $s3,$0,$t2
		
		addi $t1,$t1,1
		j loop2
		
	else2:
		addi $t1,$t1,1
		j loop2
		
	x:
		beq $s4,$0,xx
		j found
			xx:
			beq $s3,$0,noSec	# 0,0,0,...	small 0	 sec 0
			j control
		
		
			
control:
#sec is 0
	beq $t5,$s1, noSec	#if control is done and
				#no element is equal to zero, so all of them are same
	
	sll $t0,$t5,2		#to increase address
	add $t6,$t0,$s0
	lw $t2,($t6)		# values[j] = t2
	
	beq $t2,$0,found	#we know array is not 0,0,...
				#so if values[j] is 0, sec is really 0
	addi $t5,$t5,1
	j control

found:
	li $v0, 4
	la $a0, string
	syscall
	
	li $v0, 1
	add $a0,$0,$s4
	syscall
	j Exit
	
noSec:
	li $v0, 4
	la $a0, noSecond
	syscall
	j Exit

Exit:


#if you find the second smallest print it 
#if all the numbers in the array are the same print "No second smallest"
