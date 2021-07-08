import numpy as np

def write_fibo(x: int, a=0, b=1):
	if x == 0:
		return
	print(a + b)
	tmp = a
	a = b
	b = tmp + b
	write_fibo(x-1, a=a, b=b)

print("Hello world")
write_fibo(5)