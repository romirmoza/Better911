import flask
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template

import folium

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    map = folium.Map(location=[39.29, -76.61], zoom_start=11)
    folium.GeoJson(
            './static/Baltimore_City_Police_District_Boundary_Map.geojson',
            name='geojson'
            ).add_to(map)
    map.save('./static/map.html')
    return render_template('index.html')

@app.route('/static/map.html')
def show_map():
    return flask.send_file('./static/map.html')

if __name__ == "__main__":
    app.run(debug=True)
