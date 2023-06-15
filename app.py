from flask import Flask, render_template, request, redirect, jsonify, make_response
import random
from indexcalculation import etf_returns

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
            "Symbolz",
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
    return render_template("index.html", name=set[0], default=set[1:])


@app.route("/result", methods=["POST"])
def result():
    req = request.form.to_dict(flat=False)
    total_weight = sum(float(w) for w in req["weight"])
    result = etf_returns(
        {s: float(w) / total_weight for s, w in zip(req["symbol"], req["weight"])}
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
