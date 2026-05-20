import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

@app.route("/contact")
def MaPremiereAPI():
    return render_template('contact.html')

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.get("/regions-temperature")
def api_regions_temperature():

    regions = [
        {"name": "Île-de-France",           "latitude": 48.8566, "longitude": 2.3522},
        {"name": "Auvergne-Rhône-Alpes",    "latitude": 45.7597, "longitude": 4.8422},
        {"name": "Nouvelle-Aquitaine",       "latitude": 44.8378, "longitude": -0.5792},
        {"name": "Occitanie",               "latitude": 43.6047, "longitude": 1.4442},
        {"name": "Hauts-de-France",         "latitude": 50.6292, "longitude": 3.0573},
        {"name": "Grand Est",               "latitude": 48.5734, "longitude": 7.7521},
        {"name": "Provence-Alpes-Côte d'Azur", "latitude": 43.2965, "longitude": 5.3698},
        {"name": "Pays de la Loire",        "latitude": 47.2184, "longitude": -1.5536},
        {"name": "Normandie",               "latitude": 49.1829, "longitude": -0.3707},
        {"name": "Bretagne",                "latitude": 48.1173, "longitude": -1.6778},
        {"name": "Bourgogne-Franche-Comté", "latitude": 47.2805, "longitude": 5.9993},
        {"name": "Centre-Val de Loire",     "latitude": 47.9029, "longitude": 1.9093},
        {"name": "Corse",                   "latitude": 42.0396, "longitude": 9.0129},
    ]

    result = []

    for region in regions:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={region['latitude']}"
            f"&longitude={region['longitude']}"
            "&hourly=temperature_2m"
            "&forecast_days=1"
        )
        response = requests.get(url)
        data = response.json()

        temps = data.get("hourly", {}).get("temperature_2m", [])
        temps = [t for t in temps if t is not None]
        avg_temp = round(sum(temps) / len(temps), 1) if temps else None

        result.append({
            "region": region["name"],
            "latitude": region["latitude"],
            "longitude": region["longitude"],
            "avg_temperature_c": avg_temp,
        })

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme")
def histogramme():
    return render_template("histogramme.html")

@app.route("/map")
def map():
    return render_template("map.html")

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
