from flask import Flask, render_template, request
import json

app = Flask(__name__)

def corrosion_to_score(level):
    return {"low": 1, "medium": 2, "high": 3, "excellent": 4, "good": 2}.get(level.lower(), 0)

def cost_to_score(level):
    return {"low": 1, "medium": 2, "high": 3}.get(level.lower(), 0)

def load_materials():
    with open("materials.json") as file:
        return json.load(file)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = {
            "tensile_strength": int(request.form["tensile_strength"]),
            "temperature_limit": int(request.form["temperature_limit"]),
            "corrosion_resistance": request.form["corrosion_resistance"],
            "density": float(request.form["density"]),
            "cost": request.form["cost"],
            "hardness": int(request.form["hardness"]),
            "thermal_conductivity": float(request.form["thermal_conductivity"]),
            "electrical_conductivity": float(request.form["electrical_conductivity"]),
            "recyclable": request.form["recyclable"]
        }

        materials = load_materials()
        matched = []

        for m in materials:
            # Corrosion: allow equal or better (higher score is better)
            # Cost: allow equal or cheaper (lower score is better)
            if (
                m["tensile_strength"] >= user_input["tensile_strength"] and
                m["temperature_limit"] >= user_input["temperature_limit"] and
                corrosion_to_score(m["corrosion_resistance"]) >= corrosion_to_score(user_input["corrosion_resistance"]) and
                m["density"] <= user_input["density"] and
                cost_to_score(m["cost"]) <= cost_to_score(user_input["cost"]) and
                m["hardness"] >= user_input["hardness"] and
                m["thermal_conductivity"] >= user_input["thermal_conductivity"] and
                m["electrical_conductivity"] >= user_input["electrical_conductivity"] and
                m["recyclable"].lower() == user_input["recyclable"].lower()
            ):
                matched.append(m)

        return render_template("result.html", materials=matched, criteria=user_input)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
