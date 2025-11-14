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
import uvicorn

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
            <p>This is the first version of the prototype</p>
            <a href="#learn-more" class="btn">Learn More</a>
        </header>

        <section id="learn-more">
            <h2>About</h2>
            <p>info about project.</p>
        </section>

        <footer>
            <p>&copy; 2025 CHeckpoint</p>
        </footer>
    </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)


