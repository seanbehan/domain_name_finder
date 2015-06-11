from flask import Flask, Response, request
from lib import domains

app = Flask(__name__)

@app.route("/")
def home():
    return "<form method='get' action='/results'><input type='text' name='url' placeholder='http://...'><button>Go</button></form>"

@app.route("/results")
def results():
    url = request.args.get('url')
    return Response(domains(url), mimetype='text/html', status=200)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
