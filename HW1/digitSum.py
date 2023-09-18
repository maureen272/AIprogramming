def digitSum(n):
	sum = 0
	while(n>0):
		sum += n % 10
		n = n // 10
		
	return sum


result = 0
for i in range(1, 1000001):
	result += digitSum(i)
print(f"The sum of the digits in the numbers from 1 to one million is {result:,}.")	
