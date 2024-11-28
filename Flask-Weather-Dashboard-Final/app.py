import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def weather_dashboard():
    return render_template('home.html')

@app.route('/results', methods=['POST'])
def render_results():
    location_type = request.form['locationType']
    location_input = request.form['locationInput']
    api_key = get_api_key()

    if location_type == "zip":
        zip_code, country_code = location_input.split(',')
        data = get_weather_by_zip(zip_code.strip(), country_code.strip(), api_key)
    elif location_type == "city":
        data = get_weather_by_city(location_input.strip(), api_key)
    else:
        data = {}

    # Check for valid data
    if data.get("cod") != 200:
        location = "Unknown"
        temp = "Unknown"
        feels_like = "Unknown"
        weather = "Unknown"
    else:
        location = data.get("name", "Unknown")
        temp = "{0:.2f}".format(data["main"].get("temp", 0))
        feels_like = "{0:.2f}".format(data["main"].get("feels_like", 0))
        weather = data["weather"][0].get("main", "Unknown")

    return render_template('results.html',
                           location=location, temp=temp,
                           feels_like=feels_like, weather=weather)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_by_zip(zip_code, country_code, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&units=imperial&appid={api_key}"
    response = requests.get(api_url)
    return response.json()

def get_weather_by_city(city_name, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={api_key}"
    response = requests.get(api_url)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
