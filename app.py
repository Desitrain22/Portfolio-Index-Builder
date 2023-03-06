from flask import Flask, render_template, request, jsonify
import pandas as pd
from indexcalculation import etf_returns

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    result = request.form.to_dict(flat=False)
    print(
        etf_returns(
            {
                result["symbol"][i]: result["weight"][i]
                for i in range(len(result["symbol"]))
            }
        )
    )
    return render_template("index.html")


#    if request.method == 'POST':
#        name = request.form['name']

if __name__ == "__main__":

    app.run(debug=True)
