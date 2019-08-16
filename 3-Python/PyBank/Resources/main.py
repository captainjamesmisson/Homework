import os
import csv

csvpath = os.path.join("..", "Resources", "budget_data.csv")

monthly_change = []
date = []

month = 0
first_mo_profit = 0
total_profit = 0
previous_profit = 0

with open(csvpath,'r', newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    next(csvreader)

    for row in csvreader:
      date.append(row[0])
      month = month + 1
      total_profit += int(row[1])
      profit_change = int(row[1])-previous_profit
      previous_profit = int(row[1])
      monthly_change_profit = profit_change
      monthly_change.append(profit_change)
    
    monthly_change.pop(0)
    
    max_increase_profit = max(monthly_change)
    max_increase_date = date[monthly_change.index(max_increase_profit)]
    max_decrease_profit = min(monthly_change)
    max_decrease_date = date[monthly_change.index(max_decrease_profit)]

average_change_profit = round(sum(monthly_change)/(month-1),2)
 
print("Financial Analysis")
print("--------------------")
print(f"Total # of Months: {month}")
print(f"Total Profits: ${total_profit}")
print(f"Average Monthly Change in Profits: ${average_change_profit}")
print(f"Greatest Increase in Profits:  {max_increase_date} ${max_increase_profit}")
print(f"Greatest Decrease in Profits: {max_decrease_date} ${max_decrease_profit}")

textpath = os.path.join("..", "Resources", "main.txt")

with open(textpath,'w') as text:

  text.write("Financial Analysis" + "\n")
  text.write("--------------------\n")
  text.write(f"Total # of Months: {month} \n")
  text.write(f"Total Profits: ${total_profit} \n")
  text.write(f"Average Monthly Change in Profits: ${average_change_profit} \n")
  text.write(f"Greatest Increase in Profits:  {max_increase_date} ${max_increase_profit} \n")
  text.write(f"Greatest Decrease in Profits: {max_decrease_date} ${max_decrease_profit} \n") 