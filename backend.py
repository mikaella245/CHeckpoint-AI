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
        <title>CHeckpoint </title>
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
            <style>
            .faq-item {
                margin-bottom: 15px;
                border-radius: 8px;
                background: #ffffff;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                overflow: hidden;
            }

            .faq-question {
                 width: 100%;
                 padding: 18px;
                 border: none;
                 background: #007BFF;
                 color: #fff;
                 text-align: left;
                 font-size: 16px;
                 font-weight: bold;
                 cursor: pointer;
                 outline: none;
           }

            .faq-answer {
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease;
                background: #fafafa;
                padding: 0 18px;
            }

            .faq-answer p {
                margin: 15px 0;
            }
    </style>

    
    


    </head>
    <body>
        <header>
            <h1>CHeckpoint ⚖️</h1>
            <h2>Contesting your rent does not have to be painful. </h2>
            <a href="#learn-more" class="btn">Learn More</a>
    
        </header>

        <section id="learn-more">
            <h2>Learn More</h2>
            <h3> You deserve to feel confident, not lost when dealing with rent, landlords, and régies.</h3>
            <p>CHeckpoint helps you understand your rights clearly, calmly, and without legal jargon. Just facts that finally make sense.
            Most tenants don't realise how much power they actually have or often that they're paying more than they should. With CHeckpoint 
            you get clarity, support and the confidence to make informed decisions about your home. </p>

            <p>It's not about starting a fight (and it never was).</p>
            <h4>It's about finally feeling in control </h4>

            <p>Wether you're wondering if your rent is fair, confused by your régie's latest letter, or just want to know what you can ask for</p>
            <h4>this is a safe place to explore your options and take informed action. </h4>
            <a href="#faq" class="btn"> Frequently Asked Questions</a>
        
        <section id="quiz-prompt">
        <h2>Think you know your tenant rights? Take the quiz to find out! </h2>
        <a href="/quiz" class="btn">Take the Quiz</a>

        <section id="calculator-prompt">
        <h2>Calculate how much you might be overpaying</h2>
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
        
        <section id="faq" style="padding: 50px 20px; max-width: 800px; margin: auto;">
            <h2 style="text-align:center; margin-bottom: 30px;">Frequently Asked Questions</h2>

            <div class="faq-item">
                 <button class="faq-question">What is CHeckpoint?</button>
                <div class="faq-answer">
                  <p>CHeckpoint is a tool that simplifies Swiss tenancy law so both tenants and landlords know exactly what they can and cannot do. This is a first prototype!</p>
                </div>
            </div>

            <div class="faq-item">
                <button class="faq-question">When is a rent abusive?</button>
                <div class="faq-answer">
                   <p> Abusive is any rent that exceeds more than 15% the rent required for similar houses. The comparison crtiteria in particular are the placement, the surface, the state, the equipement and the age of the house. (CO Art. 269)</p>
                </div>
            </div>

            <div class="faq-item">
                <button class="faq-question">In which cases is a rent increase invalid?</button>
                <div class="faq-answer">
                    <p>A rent increase is invalid if:</p>
                    <p> a. It was not communicated using the official form determined by the canton.</p>
                    <p> b. The motive for the increase is not stated. Meaning the landlord did not clarify why they are raising the rent.</p>
                    <h4> c. It was accompanied by a termination or threat of termination if the tenant does not accept the increase. </h4><p> Meaning that it is ILLEGAL for a landlord to threaten a tenant with eviction if they do not accept a rent increase. (CO Art. 269g)</p>
                </div>
            </div>

        
        </section>
        <script>
        const questions = document.querySelectorAll('.faq-question');

        questions.forEach(btn => {
            btn.addEventListener('click', () => {
                 const answer = btn.nextElementSibling;

                if (answer.style.maxHeight) {
                    answer.style.maxHeight = null;
                } else {
                    answer.style.maxHeight = answer.scrollHeight + "px";
                }
            });
        });
        </script>
        <footer>
            <p>&copy; 2025 CHeckpoint</p>
        </footer>
    </body>
    </html>
    """

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page():
    
    return """
    <html>
    <head>
        <title>Tenant Quiz</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #f2f2f2;
            }

            .quiz-container {
                display: flex;
                justify-content: center;
                padding: 40px 10px;
            }

            iframe {
                width: 100%;
                max-width: 720px;   
                height: 900px;      
                border: none;
                background: white;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }

            a.back {
                display: block;
                margin: 20px auto;
                text-align: center;
                color: #007BFF;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="quiz-container">
            <iframe 
                src="https://docs.google.com/forms/d/e/1FAIpQLSfLYzuZa4CNPm5J8D6NVvjTZ8UbTnZXP_UrpT79Z6H49cbUhQ/viewform?embedded=true"
                allowfullscreen>
            </iframe>
        </div>

        <a href="/" class="back">⬅ Back to Home</a>
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

           <h3> What are my options? </h3>
              <p> If you believe your rent is unfair you can contest it in the 30 days from getting your keys or in the 30 days after an increase is comminicated.</p>
              <p> You can do this by sending a letter to your régie or landlord explaining why you believe the rent is unfair. </p>
              <p> Use our AI powered letter generator to help you write a legally-backed letter adapted to your situation. </p>
              <h4>Contesting your rent has never been this quick and easy. (comming soon)</h4>
              <p> Want to know more about how to contest your rent? Do you have other questions?</p>
             <h4> Our chatbot CHarly has the answer for you. (comming soon)</h4> 
           <a href="/" class="btn">Back to Home</a>
        </div>
    </section>
    <footer>
            <p>&copy; 2025 CHeckpoint</p>
    </footer>

    </body>
    </html>
    """)
