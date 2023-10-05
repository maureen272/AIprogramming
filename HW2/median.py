n = int(input("How many numbers do you want to enter? "))

num_lst = []
for i in range(n):
	num = float(input("Enter a number: "))
	num_lst.append(num)

num_lst.sort()

mid = int(len(num_lst)/2)
if(len(num_lst) % 2 == 1):
	print("Median : %.1f" % float(num_lst[mid]))
else:
    median = (num_lst[mid] + num_lst[mid-1])/2.0
    print("Median : %.1f" % median)