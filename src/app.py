from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route("/")
def hello():

    return "Ball In Court"

@app.route("/test")
def render():

	return "coolio"

@app.errorhandler(404)
def render(error):

	return "Oh no... I found nothing"

if __name__ == "__main__":
	# NOTE: debug mode necessary if you want to see live reloads
    app.run(debug = True, host='0.0.0.0', port=80)

