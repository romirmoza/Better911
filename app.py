from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
        return "Welcome to Better911!"

if __name__ == "__main__":
    app.run()
