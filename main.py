from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import io
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})




# @app.route('/get_temperature')
# def get_temperature():

#     chart = create_temperature_chart()

@app.route('/get_liquids')
def get_liquids():
    liquids = [("Water", 4190, 997), ("Linseed oil", 1840, 924), ("Kerosene", 2100, 820)]
    result = []
    for x,y,z in liquids:
        result.append({
            'name': x,
            'heatSpecific': y,
            'density': z
        })

    return jsonify(result)

@app.route('/get_water_temperature')
def get_water_temperature():
    heat_coefficiency = int(request.args.get('heatCoefficiency'))
    heat_specific = int(request.args.get('heatSpecific'))
    heat_transmission_area = int(request.args.get('heatArea'))
    initial_temp = int(request.args.get('startTemp'))
    timestamp = int(request.args.get('timestamp'))
    temperature_limit = int(request.args.get('targetTemp'))
    volume = int(request.args.get('startVolume')) /1000
    density = int(request.args.get('density'))

    mass = volume * density
    y = 0
    result = []
    time_current = 0

    while y < temperature_limit:
        y = (heat_coefficiency * heat_transmission_area * time_current) / (mass * heat_specific) + y
        #result.append((y, time_current))
        result.append({
            'temperature': y,
            'time': time_current
        })
        time_current += timestamp

    return jsonify(result)

@app.route('/get_live_simulation')
def get_live_simulation():
    heat_coefficiency = int(request.args.get('heatCoefficiency'))
    heat_specific = int(request.args.get('heatSpecific'))
    heat_transmission_area = int(request.args.get('heatArea'))
    mass = int(request.args.get('mass'))
    volume_in = int(request.args.get('volIn')) /1000
    volume_out = int(request.args.get('volOut')) /1000
    volume_old = int(request.args.get('startVolume')) /1000
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

    #return jsonify((volume_current, time_current, temperature_2))
    result = {
        'volume': volume_current,
        'time': time_current,
        'temperature': temperature_2
    }

    return jsonify(result)

def create_chart():
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    xs = range(100)
    ys = [random.randint(1,50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == '__main__':
    app.run(debug=True)