import flask
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request

import pandas as pd
import dill
import folium
from bokeh.embed import components
from bokeh.plotting import figure
from wtforms import Form, SelectField, SubmitField

app = Flask(__name__)
bootstrap = Bootstrap(app)

class PlotInputForm(Form):
    district = SelectField('District', choices=[('Northern', 'Northern'),
                                                ('Central', 'Central'),
                                                ('Eastern', 'Eastern'),
                                                ('Northeastern', 'Northeastern'),
                                                ('Northern', 'Northern'),
                                                ('Northwestern', 'Northwestern'),
                                                ('Southeastern', 'Southeastern'),
                                                ('Southern', 'Southern'),
                                                ('Southwestern', 'Southwestern'),
                                                ('Western', 'Western')])
    priority = SelectField('Priority', choices=[('Medium', 'Medium'),
                                                ('Emergency', 'Emergency'),
                                                ('High', 'High'),
                                                ('Low', 'Low'),
                                                ('Non-Emergency', 'Non-Emergency')])
    submit = SubmitField("Plot")

def plot_prediction(data, model, district, priority):
    d = data[data.Priority == priority]
    d = d[d.PoliceDistrict == district]
    d['Count_Predict'] = model.predict(d)
    d = d.sort_values(by=['CallDateTime'])

    fig = figure(width=800, height=800, x_axis_type='datetime', align = 'center')
    fig.xaxis.axis_label = 'Date'
    fig.yaxis.axis_label = 'Emergency count'

    fig.circle(x='CallDateTime', y='Count', source=d, color='grey')
    fig.line(x='CallDateTime', y='Count_Predict', source=d, line_width=3, color='red')
    return fig

@app.route('/', methods = ['GET', 'POST'])
def index():
    map = folium.Map(location=[39.29, -76.61], zoom_start=11)
    folium.GeoJson(
            './static/Baltimore_City_Police_District_Boundary_Map.geojson',
            name='geojson'
            ).add_to(map)
    map.save('./static/map.html')

    data = pd.read_pickle("./static/weekly_data.pkl")
    dill._dill._reverse_typemap['ClassType'] = type
    model = dill.load(open('./static/model_julian_weekly.dill', 'rb'))

    form = PlotInputForm()
    if request.method == 'POST':
        form = PlotInputForm(request.form)
        plot = plot_prediction(data, model, form.district.data, form.priority.data)
        script, div = components(plot)
        return render_template('index.html', scroll="form", form=form, script=script, div=div)
    return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/static/map.html')
def show_map():
    return flask.send_file('./static/map.html')

if __name__ == "__main__":
    app.run(debug=True)
