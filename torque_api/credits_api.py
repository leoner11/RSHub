from flask import Flask, request, jsonify, Response

app = Flask(__name__)

class CreditAPI:
    def __init__(self):
        self.current_credits = 100
        self.path = ""

    def check_credits(self, path):
        return jsonify({'current_credits': self.current_credits,  "path": path})

    def subtract_credits(self, substracter, path):
        self.current_credits -= substracter
        return jsonify({'current_credits': self.current_credits, "path": path})

credit_api = CreditAPI()

# IF WANT TO CHECK HOW MANY CREDITS ARE NEEDED
@app.route('/check_credits', methods=['GET'])
def check_credits(path):
    return credit_api.check_credits()


# THIS WILL BE CALLED WHEN THE SERVER WANTS TO CHECK WHETHER THE FUNCTION CAN BE RUN
@app.route('/subtract_credits', methods=['POST'])
def subtract_credits():
    data = request.json
    substracter = data.get('substracter', 0)
    if credit_api.current_credits < substracter:
        return jsonify({"message": "Credits are not enough"}), 400
    else:
        return credit_api.subtract_credits(substracter)

# CALL IF YOU WANT TO ADD THE CREDITS
@app.route('/add_credits', methods=['POST'])
def add_credits(path):
    data = request.json
    credits = data.get('credits', 0)
    credit_api.current_credits += credits
    return jsonify({'current_credits': credit_api.current_credits,  "path": path})

if __name__ == '__main__':
    app.run(debug=True)
