futureValue = int(input("Enter future value: "))
interestRate = float(input("Enter interest rate (as %): "))
years = int(input("Enter number of years: "))

presentValue = futureValue / ((1 + interestRate/100) ** years)


print("Present value: ${:,.2f}".format(presentValue))
