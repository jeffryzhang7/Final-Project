from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

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


# Function to fetch real estate listings
def fetch_real_estate_listings(api_key):
    url = "http://sandbox.repliers.io"  
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to find closest listings
def find_closest_listings(listings, loan_amount):
    if not listings:
        return []
    
    sorted_listings = sorted(listings, key=lambda x: abs(x['price'] - loan_amount))
    return sorted_listings[:3]

# Route for handling the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    closest_listings = None
    if request.method == 'POST':
        principal = float(request.form.get('principal'))
        annual_interest_rate = float(request.form.get('interest_rate'))
        years = int(request.form.get('years'))

        results = {
            'fixed_payments': calculate_fixed_payments(principal, annual_interest_rate, years),
            'equal_principal': calculate_equal_principal_payments(principal, annual_interest_rate, years)
        }

        # Fetch and find closest real estate listings
        api_key = "GC31wP1JzCdNgf7LxqQsLqUIG6f3di" 
        listings = fetch_real_estate_listings(api_key)
        closest_listings = find_closest_listings(listings, principal)

    return render_template_string(PAGE_HTML, results=results, listings=closest_listings)

if __name__ == '__main__':
    app.run(debug=True)

PAGE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <title>Housing Loan Calculator</title>
  </head>
  <body>
    <h1>Housing Loan Payment Calculator</h1>
    <form method="post">
      <!-- Form fields -->
      <!-- ... [existing form fields] ... -->
      <input type="submit" value="Calculate">
    </form>
    {% if results %}
      <!-- Results display -->
      <!-- ... [existing results display] ... -->
    {% endif %}
    {% if listings %}
      <h2>Closest Real Estate Listings</h2>
      <ul>
        {% for listing in listings %}
          <li>
            Address: {{ listing['address'] }}, Price: {{ listing['price'] }}, MLS Number: {{ listing['mlsNumber'] }}
          </li>
        {% endfor %}
      </ul>
    {% endif %}
  </body>
</html>
"""
