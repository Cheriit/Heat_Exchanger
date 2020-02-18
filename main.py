from flask import Flask, send_file

app = Flask(__name__)

@app.route('/get_chart')
def get_chart():
    return send_file('testpic.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)