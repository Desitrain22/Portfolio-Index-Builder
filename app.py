import random
from flask import Flask, render_template, request, jsonify, make_response
from indexcalculation import index_returns, portfolio_returns, get_symbol_universe
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    samples = [
        [
            "MANGA Index",
            ("META", 0.2),
            ("AAPL", 0.2),
            ("NFLX", 0.2),
            ("GOOG", 0.2),
            ("AMZN", 0.2),
        ],
        [
            "Becky Index",
            ("LULU", 25),
            ("ADBE", 15),
            ("SBUX", 35),
            ("AAPL", 20),
            ("PTON", 5),
        ],
        [
            "Funny Symbolz",
            ("PZZA", 3),
            ("YUM", 3),
            ("SHOO", 10),
            ("SIX", 3),
            ("ROCK", 3),
            ("LUV", 10),
            ("JOB", 10),
            ("FROG", 5),
            ("COKE", 10),
            ("BBW", 69),
        ],
    ]
    set = samples[random.randint(0, len(samples) - 1)]
    symbols = get_symbol_universe()
    return render_template("index.html", name=set[0], default=set[1:], symbols=symbols)


@app.route("/result", methods=["POST"])
def result():
    req = request.form.to_dict(flat=False)
    print(req)
    total_weight = sum(float(w) for w in req["weight"])
    if req["rebalance_type"] == ["index"]:
        result = index_returns(
            {s: float(w) / total_weight for s, w in zip(req["symbol"], req["weight"])},
            start_date=pd.Timestamp(req["startDate"][0], tz="US/Pacific"),
        )
    else:
        result = portfolio_returns(
            {s: float(w) / total_weight for s, w in zip(req["symbol"], req["weight"])},
            start_date=pd.Timestamp(req["startDate"][0], tz="US/Pacific"),
        )
    print(result)

    res = make_response(
        jsonify(
            {
                "dates": list(result.index),
                "values": list(result["Index"]),
            }
        ),
        200,
    )
    print(res)
    return res


if __name__ == "__main__":
    app.run(debug=True)
