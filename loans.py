amount_owe = int(input("what is the loan amount?\n"))
bir = float(input("what is the bank interest rate ?\n"))
emi_ready_to_pay = int(input("how much EMI will you pay ?\n"))
months = int(input("how many months of loan ?\n"))

monthly_rate = bir/100/12


for i in range(months):
  interest_paid = amount_owe*monthly_rate
  amount_owe = amount_owe + interest_paid

  if (round(amount_owe)-emi_ready_to_pay) < 0:
    print("the money owed is ", round(amount_owe))
    print("you paid off the loan in ", i+1, " months") # thats because i the month in range starts from 0
    break
  
  amount_owe = amount_owe - emi_ready_to_pay

  print("Paid ", emi_ready_to_pay, 'of which', round(interest_paid), ' was interest', end = ' ')
  print('Balance is', round(amount_owe))