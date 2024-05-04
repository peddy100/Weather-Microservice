import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = 'b428b4c6635256e5ac6a1f87c1b55f8f'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    date = request.args.get('date')

    if not city:
        return jsonify({"error": "City parameter is missing."}), 400
    if not date:
        return jsonify({"error": "Date parameter is missing."}), 400

    params = {'q': city, 'appid': API_KEY, 'units': 'imperial'}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        forecast = filter_forecast(weather_data, date)
        if forecast:
            return jsonify(forecast), 200
        else:
            return jsonify({"error": "Weather forecast not found for the specified date. Please check that date is "
                                     "within 5 days from Today"}), 404
    else:
        return jsonify({"error": "Weather data not found for city. Please check spelling"}), 404


def filter_forecast(weather_data, date):
    for item in weather_data['list']:
        # Check if the item's 'dt_txt' matches the specified date
        if item['dt_txt'].startswith(date):
            temperature = item['main']['temp']
            temp_max = item['main']['temp_max']
            temp_min = item['main']['temp_min']
            description = item['weather'][0]['description']
            wind = item['wind']

            weather_info = {
                "Date": item['dt_txt'],
                "Temp": temperature,
                "Max Temp": temp_max,
                "Min Temp": temp_min,
                "Description": description,
                "Wind": wind
            }

            return weather_info

    return None


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
