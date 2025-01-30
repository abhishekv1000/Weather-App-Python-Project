from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

# FastAPI app
app = FastAPI()

# Set up static files (to serve CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates (to serve HTML)
templates = Jinja2Templates(directory="templates")

# OpenWeatherMap API key
API_KEY = "8e3abd7485e4d5afc62b907e560d6045"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data from OpenWeatherMap
def get_weather_data(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en",
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    return response.json()

# Route to serve the HTML form and handle the weather result
@app.get("/", response_class=HTMLResponse)
async def get_weather_form(request: Request, city: str = None):
    weather_info = None
    if city:
        try:
            data = get_weather_data(city)
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "weather": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
            }
        except HTTPException as e:
            weather_info = {"error": e.detail}

    return templates.TemplateResponse("weather_form.html", {"request": request, "weather_info": weather_info})
