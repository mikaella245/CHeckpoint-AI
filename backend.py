#from fastapi import FastAPI, Request
#from fastapi.responses import HTMLResponse
#from fastapi.staticfiles import StaticFiles
#from fastapi.templating import Jinja2Templates
#import os

#app = FastAPI()
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve static files (CSS, JS, images)
#app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Setup templates
#templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Landing page route
#@app.get("/", response_class=HTMLResponse)
#async def landing_page(request: Request):
    #return templates.TemplateResponse("index.html", {"request": request})


from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from logic import calculate_faireness
from models import RentInput 

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>CHeckpoint</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                text-align: center;
                background-color: #f2f2f2;
            }
            header {
                background-color: #007BFF;
                color: white;
                padding: 50px 0;
            }
            header .btn {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: white;
                color: #007BFF;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            section {
                padding: 50px 20px;
            }
            section .btn {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: white;
                color: #007BFF;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            footer {
                background-color: #333;
                color: white;
                padding: 20px;
            }
        </style>


    </head>
    <body>
        <header>
            <h1>CHeckpoint</h1>
            <p>Is rent one of the biggest expenses in your life? Do you live in constant fear of the next rent increase?</p>
            <p>You are not alone.</p>
            <a href="#learn-more" class="btn">Learn More</a>
    
        </header>

        <section id="learn-more">
            <h2>Learn More</h2>
            <p>Did you know that Swiss tenants OVERpay an estimated 14 BILLION CHF in rent every year? This significant amount is mainly due to a lack of automatic adaptation 
            of rents to the current taux de référence and abusive practices by some landlords.</p>
        
        
        <section id="calculator-prompt">
        <h2>Want to know how affected you are?</h2>
            <a href="#rent-calculator" class="btn">Rent Faireness Calculator</a>
        </section>

        <section id="rent-calculator">
            <h2>Rent Calculator</h2>
            <form method="post" action="/check_rent/calculate">
                <label>Original Rent (CHF):
                <input type="number" step="0.01" name="original_rent" placeholder="Original Rent (CHF)" required>
                <label>Current Rent (CHF):
                <input type="number" step="0.01" name="current_rent" placeholder="Current Rent (CHF)" required>
                <label>Year the contract was signed:
                <input type="number" name="contract_year" placeholder="Year" required>
                <label>Year the increase took place:
                <input type="number" name="increase_year" placeholder="Year" required>
                <label>Were there any renovations done before the increase?:
                <select name="renovations">
                    <option value="True">Yes</option>
                    <option value="False">No</option>
                </select>
                <button type="submit">Calculate</button>
            </form>
        </section>

        <footer>
            <p>&copy; 2025 CHeckpoint</p>
        </footer>
    </body>
    </html>
    """
@app.post("/check_rent/calculate")
async def calculate_rent(
    original_rent: float = Form(...),
    current_rent: float = Form(...),
    contract_year: int = Form(...),
    increase_year: int = Form(...),
    renovations: str = Form(...),
):
    
    rent_data = RentInput(
        original_rent=original_rent,
        current_rent=current_rent,
        contract_year=contract_year,
        increase_year=increase_year,
        renovations= True if renovations == "True" else False,

    )
    result = calculate_faireness(rent_data)
    #total_max_rent = result["allowed_rent_estimate"]
    #difference = result["difference"]
    #evaluation = result["evaluation"]

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Rent Fairness Result</title>
        <style>
           body {{
               font-family: Arial, sans-serif;
               margin: 0;
               padding: 0;
               background-color: #f2f2f2;
               text-align: center;
            }}
             header {{
               background-color: #007BFF;
               color: white;
               padding: 40px 0;
            }}
             header h1 {{
               margin: 0;
               font-size: 32px;
            }}
             section {{
               padding: 40px 20px;
            }}
             .result-box {{
                background-color: white;
                max-width: 500px;
                margin: auto;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
             footer {{
                background-color: #333;
                color: white;
                padding: 20px;
            }}         
            .btn {{
                display: inline-block;
                margin-top: 25px;
                padding: 12px 25px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }}
    </style>
    </head>

    <body>

    <header>
       <h1>Rent Fairness Result</h1>
    </header>

    <section>
        <div class="result-box">

           <p><strong>Maximum Allowed Rent Estimate:</strong> {result["allowed_rent_estimate"]} CHF</p>
           <p><strong>Difference between Allowed and Current Rent:</strong> {result["difference"]} CHF</p>
           <p><strong>Assessment:</strong> {result["assessment"]}</p>

           <a href="/" class="btn">Back to Home</a>
        </div>
    </section>
    <footer>
            <p>&copy; 2025 CHeckpoint</p>
    </footer>

    </body>
    </html>
    """)
