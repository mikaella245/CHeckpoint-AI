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


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from router import router
import uvicorn

app = FastAPI()
app.include_router(router, prefix = "/rent-calculator")

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
            <a href="#rent-calculator" class="btn">Rent Faireness Calculator</a
        </section>

        <section id="rent-calculator">
            <h2>Rent Calculator</h2>
            <form method="post" action="/calculate"> <!-- make sure your router route is /calculate -->
                <input type="number" step="0.01" name="original_rent" placeholder="Original Rent (CHF)" required>
                <input type="number" step="0.01" name="current_rent" placeholder="Current Rent (CHF)" required>
                <input type="number" name="contract_year" placeholder="Contract Year" required>
                <input type="number" name="increase_year" placeholder="Increase Year" required>
                <label>Renovations:
                    <select name="renovations">
                        <option value="True">Yes</option>
                        <option value="False">No</option>
                    </select>
                </label>
                <input type="number" step="0.01" name="inflation_rate" placeholder="Inflation Rate (%)" required>
                <button type="submit">Calculate</button>
            </form>
        </section>

        <footer>
            <p>&copy; 2025 CHeckpoint</p>
        </footer>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)




