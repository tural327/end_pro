from flask import Flask

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World from Elastic Beanstalk  Tural🚀"

@application.route("/health")
def health():
    return {"status": "ok"}, 200
