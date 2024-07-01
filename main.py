from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hiiiii'


def get_city(ip_address):
    print("Client IP: ", ip_address)
    ipfind_api_key = '811d1e15-1741-4f72-95bf-2415c53c9dce'
    #ipfind_url = f'https://ipfind.co/?auth={ipfind_api_key}&ip={ip_address}'
    ipfind_url = f'https://api.ipfind.com?ip=105.112.33.234&auth={ipfind_api_key}'
    response = requests.get(ipfind_url)
    response_data = response.json()
    print("Ipfind response:", response_data)  # Log Ipfind response for debugging
    city_name = response_data.get('city', 'City Not Found')
    return city_name

def get_temperature(city):
    openweathermap_api_key = '850403ea0ac6e2fc99c7b06643153587'
    openweathermap_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_api_key}&units=metric'
    response = requests.get(openweathermap_url)
    response_data = response.json()
    print("OpenWeatherMap response:", response_data)  # Log OpenWeatherMap response for debugging
    if response.status_code == 200:
        main_data = response_data['main']
        temperature = main_data['temp']
        return temperature
    else:
        return None



@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name')
    client_ip = request.remote_addr
    city = get_city(client_ip)
    temperature = get_temperature(city)
    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {city}"
    }
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
