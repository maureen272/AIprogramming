for num in range(1000, 10000):
		num_str = str(num)
		lst = [i for i in num_str] 
		lst.reverse()
		new_num = int("".join(lst))
		
		if(4*num == new_num):
			print("Since 4 times {} is {}, the special number is {}.".format(num, new_num, num))