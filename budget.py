class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []

  # Readable print
  def __str__(self):
    # Initialize variables
    title = self.name.center(30, "*") + "\n"
    output_string = title
    output_total = 0

    # Load descriptions and amounts
    # If description or amount are longer than the available space, shorten them
    for i in self.ledger:
      # Description
      description = i["description"]
      if len(description) > 23:
        description = description[:23]
      description = description.capitalize()

      # Amount
      amount = i["amount"]
      amount_string = str(amount)
      if len(amount_string) > 7:
        amount_string = amount_string[:7]

      # get total balance
      output_total += i["amount"]

      # Append everything to the output string
      output_string += f"{description.ljust(23)}{amount_string.rjust(7)}\n"

    # Append total balance to the output string
    output_string += f"Total: {str(output_total)} \n"

    return output_string

  # Check if there's enough funds
  def check_funds(self, amount):
    current_sum = 0
    for i in self.ledger:
      current_sum += i["amount"]

    if current_sum - amount < 0:
      return False
    return True

  # Deposit method
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})

  # Withdraw method only if there are enought funds
  # Uses deposit method to add negative amount to ledger
  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.deposit(amount * -1, description)
      return True
    else:
      return False

  # Get category balance
  def get_balance(self):
    total_balance = 0
    for i in self.ledger:
      total_balance += i["amount"]
    return total_balance

  # Auxiliary method to return only negative amounts from a category
  def get_spendings(self):
    total_spendings = 0
    for i in self.ledger:
      if i["amount"] < 0:
        total_spendings += i["amount"]
    return total_spendings

  # Transfer to another category
  # Use withdraw method to check if there are enough funds
  # And add the negative amount
  # Then deposit to the new category
  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.name}")
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    return False


# Draw the chart
def create_spend_chart(categories):

  # Initialize the variables
  chart = "Percentage spent by category\n"
  spendings = []
  max_category_length = 0
  
  # Calculate the total spent for each category and find the maximum category name length
  for category in categories:
      spendings.append(category.get_spendings())
      if len(category.name) > max_category_length:
          max_category_length = len(category.name)
  
  # Calculate the percentage spent and create the chart
  total_spending = sum(spendings)
  
  for percentage in range(100, -1, -10):
      # Generate the string
      chart += str(percentage).rjust(3) + "| "

      # Calculate if the current category's spending is bigger than the current 
      # percentage on all of the spendings
      for spending in spendings:
          bar = "o" if spending <= (total_spending / 100 * percentage) else " "
          chart += bar.rjust(1) + "  "
      chart += "\n"
  
  # Add the horizontal line after the chart
  chart += "    -" + "---" * len(categories) + "\n"
  
  # Add the category names vertically
  for i in range(max_category_length):
      chart += "     "
      for category in categories:
          if i < len(category.name):
              chart += category.name[i] + "  "
          else:
              chart += "   "
      chart += "\n"
  
  return chart
  