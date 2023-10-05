first_name = input("Enter first name: ")
last_name = input("Enter last name: ")
current_salary = float(input("Enter current salary: "))

if current_salary < 40000:
    new_salary = current_salary * 1.05
else:
    new_salary = current_salary + (current_salary - 40000) * 0.02 + 2000


result= "${:,.2f}".format(new_salary)
print("New salary for", first_name, last_name + ":", result)
