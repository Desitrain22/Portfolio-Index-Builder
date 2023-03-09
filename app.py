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
    # total_weight = sum([float(w) for w in result["weight"]])
    total_weight = sum(eval(w) for w in result["weight"])
    print(total_weight)
    print(
        etf_returns(
            {
                result["symbol"][i]: float(result["weight"][i]) / total_weight
                for i in range(len(result["symbol"]))
            }
        )
    )
    return render_template("index.html")

if __name__ == "__main__":

    app.run(debug=True)
