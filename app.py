from flask import Flask, jsonify, request
from datetime import datetime
import json, pytz, csv, re

app = Flask(__name__)
API_TOKEN = "supersecrettoken123"

def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

def get_city_data():
    city_data = {}
    with open('capitals.csv', mode='r', encoding='utf-8') as file:
        file_reader = csv.reader(file)
        next(file_reader)
        for row in file_reader:
            try:
                city = row[6].strip().lower()
                timezone_info = row[17]
                if not timezone_info:
                    print(f"Timezone data missing for {city}")
                    continue
                clean_timezones = timezone_info.replace("'", "\"").replace("\\/", "/")
                clean_timezones = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', clean_timezones)
                try:
                    timezones = json.loads(clean_timezones)
                    timezone_data = timezones[0]
                    timezone_name = timezone_data['zoneName']
                    gmt_offset = timezone_data['gmtOffsetName']
                    abbreviation = timezone_data['abbreviation']
                    city_data[city] = {
                        'timezone': timezone_name,
                        'gmt_offset': gmt_offset,
                        'abbreviation': abbreviation
                    }
                except (json.JSONDecodeError, IndexError) as e:
                    print(f"Error parsing timezone data for {city}: {e}")
                    continue
            except IndexError as e:
                print(f"Error reading data for {row}: {e}")
                continue
    return city_data

def get_current_time(city):
    city_data = get_city_data()
    city = city.lower()
    if city not in city_data:
        print(f"'{city}' not found in data set")
        return jsonify({"error": "City not found"}), 404
    timezone_info = city_data[city]
    timezone = timezone_info['timezone']
    gmt_offset = timezone_info['gmt_offset']
    abbreviation = timezone_info['abbreviation']
    try:
        zone = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        return jsonify({"error": "Timezone not valid"}), 500
    local_time = datetime.now(zone).strftime("%Y-%m-%d %H:%M:%S")
    response = {
        "city": city.capitalize(),
        "local_time": local_time,
        "utc_offset": gmt_offset,
        "abbreviation": abbreviation
    }
    return jsonify(response)

@app.route('/api/current-time/<city>', methods=['GET'])
@token_required
def current_time(city):
    return get_current_time(city)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

@app.route('/api/secure-data', methods=['GET'])
@token_required
def secure_data():
    return jsonify({"secret": "This is protected info!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)