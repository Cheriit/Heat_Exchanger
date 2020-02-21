from flask import Flask, Response, request, jsonify
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random

app = Flask(__name__)

# @app.route('/get_temperature')
# def get_temperature():

#     chart = create_temperature_chart()
    
@app.route('/get_liquids')
def get_liquids():
    liquids = [("Water", 4190, 997), ("Linseed oil", 1840, 924), ("Kerosene", 2100, 820)]
    return jsonify(liquids)

@app.route('/get_water_temperature')
def get_water_temperature():
    heat_coefficiency = int(request.args.get('heatCoefficiency'))
    heat_specific = int(request.args.get('heatSpecific'))
    heat_transmission_area = int(request.args.get('hearArea'))
    mass = int(request.args.get('mass'))
    initial_temp = int(request.args.get('startTemp'))
    timestamp = int(request.args.get('timestamp'))
    temperature_limit = int(request.args.get('targetTemp'))

    y = 0
    result = []

    while y < temperature_limit:
        y = (heat_coefficiency * heat_transmission_area * timestamp) / (mass * heat_specific) + initial_temp
        result.append(y)

    return jsonify(result)

@app.route('/get_live_simulation')
def get_live_simulation():
    heat_coefficiency = int(request.args.get('heatCoefficiency'))
    heat_specific = int(request.args.get('heatSpecific'))
    heat_transmission_area = int(request.args.get('heatArea'))
    mass = int(request.args.get('mass'))
    volume_in = int(request.args.get('volIn'))
    volume_out = int(request.args.get('volOut'))
    volume_old = int(request.args.get('startVolume'))
    time_old = int(request.args.get('timeOld'))
    timestamp = int(request.args.get('timestamp'))
    temperature_limit = int(request.args.get('targetTemp'))
    temperature_current = int(request.args.get('startTemp'))
    temperature_in = int(request.args.get('tempIn'))

    volume_current = volume_in * timestamp + volume_old - volume_out * timestamp
    time_current = time_old + timestamp

    temperature_next = (volume_in*(temperature_current - temperature_in) - temperature_current*(volume_current - volume_out)) / \
                        (volume_out - volume_current)
    
    temperature_2 = (heat_coefficiency * heat_transmission_area * timestamp) / (mass * heat_specific) + temperature_next

    return jsonify((volume_current, time_current, temperature_2))

def create_chart():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = range(100)
    ys = [random.randint(1,50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == '__main__':
    app.run(debug=True)