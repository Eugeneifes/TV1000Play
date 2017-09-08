from flask import Flask

app = Flask(__name__)

@app.route('/churn_rate', methods = ['GET'])
def samplefunction():
    with open("churn_rate.html") as html_file:
        return html_file.read()


if __name__ == '__main__':
    port = 8000
    app.run(host='0.0.0.0', port=port)