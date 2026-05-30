import os
import datetime
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# konfiguracja
AUTHOR_NAME = "Maksymilian Rachubik"
PORT = 5000
API_KEY = os.getenv("WEATHER_API_KEY")

#lokacje do wyboru
LOCATIONS = [
    {"country": "Poland", "city": "Lublin"},
    {"country": "Poland", "city": "Warsaw"},
    {"country": "United Kingdom", "city": "London"},
    {"country": "France", "city": "Paris"},
    {"country": "Germany", "city": "Berlin"},
    {"country": "Italy", "city": "Rome"}
]
#szablon html
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Pogoda</title></head>
<body>
    <h1>Wybierz lokalizację</h1>
    <form method="POST">
        <select name="location">
            {% for loc in locations %}
                <option value="{{ loc.city }}">{{ loc.city }}, {{ loc.country }}</option>
            {% endfor %}
        </select>
        <button type="submit">Sprawdź pogodę</button>
    </form>
    {% if weather %}
        <h2>Pogoda dla {{ city }}: {{ weather }} °C</h2>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    selected_city = None
    if request.method == "POST":
        selected_city = request.form.get('location')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}&units=metric"
        
        response = requests.get(url).json()
        if response.get("main"):
            weather_data = response["main"]["temp"]
    #renderowanie strony
    return render_template_string(HTML_TEMPLATE, locations=LOCATIONS, weather=weather_data, city=selected_city)

#endpoint do healthcheck
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # Punkt 1a: Informacja w logach
    print(f"Data uruchomienia: {datetime.datetime.now()}")
    print(f"Autor: {AUTHOR_NAME}")
    print(f"Port TCP: {PORT}")
    #uruchomienie na 0.0.0.0
    app.run(host='0.0.0.0', port=PORT)