coefficient = float(input("Enter coefficient of restitution: "))
initialHeight = float(input("Enter initial height in meters: "))

cnt = 1
distance = initialHeight
height = initialHeight * coefficient	
while(height >= 0.1):
	#print(height)
	distance += height*2
	cnt += 1
	height *= coefficient
	
print(f"Number of bounces: {cnt}")
print(f"Meters traveled: {distance:.2f}")