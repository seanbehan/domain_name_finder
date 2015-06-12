from flask import Flask, Response, request
from jinja2 import Template
from lib import domains

app = Flask(__name__)

@app.route("/")
def home():
    t = Template(open('home.html').read())
    return t.render(domain="")

@app.route("/results")
def results():
    url = request.args.get('url')
    return Response(domains(url), mimetype='text/html', status=200)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
