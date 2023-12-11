from flask import Flask, render_template_string, request
app = Flask(__name__)
PAGE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <title>Housing Loan Calculator</title>
  </head>
  <body>
    <h1>Housing Loan Payment Calculator</h1>
    <form method="post">
      <label for="principal">Loan Amount:</label><br>
      <input type="number" id="principal" name="principal" min="0" step="any" required><br>
      <label for="interest_rate">Annual Interest Rate (%):</label><br>
      <input type="number" id="interest_rate" name="interest_rate" min="0" max="100" step="any" required><br>
      <label for="years">Loan Period (Years):</label><br>
      <input type="number" id="years" name="years" min="1" required><br><br>
      <input type="submit" value="Calculate">
    </form>
    {% if results %}
      <h2>Results</h2>
      <h3>Equal Loan Payments (Fixed Payments):</h3>
      <ul>
        {% for payment in results['fixed_payments'] %}
          <li>{{ payment }}</li>
        {% endfor %}
      </ul>
      <h3>Equal Principal Payments:</h3>
      <ul>
        {% for payment in results['equal_principal'] %}
          <li>{{ payment }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  </body>
</html>
"""

# Function to calculate fixed payments
def calculate_fixed_payments(principal, annual_interest_rate, years):
    results = []
    monthly_interest_rate = annual_interest_rate / 12 / 100
    months = years * 12
    monthly_payment = principal * monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -months)
    remaining_principal = principal

    for month in range(1, months + 1):
        interest = remaining_principal * monthly_interest_rate
        principal_payment = monthly_payment - interest
        remaining_principal -= principal_payment
        results.append(f"Month {month}: Payment = {monthly_payment:.2f}, Remaining Principal = {remaining_principal:.2f}")
    return results

# Function to calculate equal principal payments
def calculate_equal_principal_payments(principal, annual_interest_rate, years):
    results = []
    monthly_interest_rate = annual_interest_rate / 12 / 100
    months = years * 12
    principal_payment = principal / months
    remaining_principal = principal

    for month in range(1, months + 1):
        interest = remaining_principal * monthly_interest_rate
        total_payment = principal_payment + interest
        remaining_principal -= principal_payment
        results.append(f"Month {month}: Payment = {total_payment:.2f}, Remaining Principal = {remaining_principal:.2f}")
    return results

# Route for handling the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        principal = float(request.form.get('principal'))
        annual_interest_rate = float(request.form.get('interest_rate'))
        years = int(request.form.get('years'))

        # Calculate payments
        results = {
            'fixed_payments': calculate_fixed_payments(principal, annual_interest_rate, years),
            'equal_principal': calculate_equal_principal_payments(principal, annual_interest_rate, years)
        }
    return render_template_string(PAGE_HTML, results=results)

if __name__ == '__main__':
    app.run(debug=True)

