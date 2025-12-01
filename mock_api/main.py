from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Mock Weather API",
    version="1.0.0",
    description="Simple GET-only mock weather service"
)

# ----- Models -----
class Weather(BaseModel):
    city: str
    temperature_c: float
    condition: str
    humidity: int
    time: str


# ----- Routes -----
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/weather/{city}", response_model=Weather, summary="Get weather by city")
def get_weather(city: str):
    # Mock data (randomized or static)
    return Weather(
        city=city,
        temperature_c=27.3,
        condition="Cloudy",
        humidity=70,
        time=datetime.utcnow().isoformat()
    )
