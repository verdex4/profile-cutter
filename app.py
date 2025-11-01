from flask import Flask, render_template, request, jsonify
import profile_cutter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=['POST'])
def process():
    user_input = request.form
    print(user_input)

    error_message = _validate_input(user_input)
    if error_message:
        return jsonify({'result': error_message})

    stock, demand = _to_dictionaries(user_input)
    print(f"stock: {stock}")
    print(f"demand: {demand}")

    cutter = profile_cutter.Cutter(stock, demand)
    result = cutter.calculate()
    print(result)
    
    return jsonify({'result': result})

def _validate_input(user_input):
    for key, value in user_input.items():
        if len(key) == 0 or len(value) == 0:
            return "Заполните все поля!"
    return None

def _to_dictionaries(user_input):
    stock, demand = dict(), dict()
    for key, value in user_input.items():
        if key.startswith("qty"):
            length_key = "len" + key[-1]
            corresponding_length = float(user_input[length_key])
            stock[corresponding_length] = int(value)
        elif key == "demand_qty":
            length_key = "demand_len"
            corresponding_length = float(user_input[length_key])
            demand[corresponding_length] = int(value)
    return stock, demand

if __name__ == '__main__':
    app.run()