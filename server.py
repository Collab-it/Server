from pyrebase import pyrebase
from flask import Flask, request, jsonify
import pandas as pd
import pickle
config = {
    "apiKey": "AIzaSyCfEjJpkUdFooIkdqdRj_TZng1imrmymMY",
    "authDomain": "my-portfolio-248515.firebaseapp.com",
    "databaseURL": "https://my-portfolio-248515.firebaseio.com",
    "projectId": "my-portfolio-248515",
    "storageBucket": "my-portfolio-248515.appspot.com",
    "messagingSenderId": "970529353485",
    "appId": "1:970529353485:web:529efcd5de1ede64"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)


@app.route("/", methods=['POST'])
def formInput():
    model = pickle.load(
        open("../Model.pickle", 'rb')
    )

    x = request.get_json()

    # y = model.predict([list(map(float, x.values()))])
    print(type(x))
    val = []
    val.append(int(x['age']))
    val.append(int(x['family_history'] == 'No'))
    d = {
        'Somewhat easy': 1,
        "Don't know": 1.5,
        'Very easy': 0,
        'Somewhat difficult': 2,
        'Very difficult': 3
    }
    val.append(d[x['leave']])
    d = {
        'often': 3,
        'never': 0,
        'sometimes': 7,
        'rarely': 5
    }
    val.append(d[x['work_interfere']])
    val.append(int(x['benefits'] == 'No'))
    val.append(int(x['anonymity'] == 'No'))

    d = {
        'No': 0,
        'Yes': 1,
        "Don't know": 1.5
    }
    val.append(d[x['phys_health_consequence']])

    val.append(d[x['mental_health_interview']])
    val.append(int(x['obs_consequence'] == 'No'))

    print(val)
    val2 = []
    val2.append(val)
    y = model.predict_proba(val2)
    y = y[0][0]
    data = {
        "age":val[0],
        "family_history":val[1],
        "leave":val[2],
        "work_interfere":val[3],
        "benefits":val[4],
        "anonymity":val[5],
        "phys_health_consequence":val[6],
        "mental_health_interview":val[7],
        "obs_consequence":val[8],
        "prediction":y
    }
    db.child("monthly_data").push(data)

    y1 = jsonify({
        "prediction": y
    })  # Data snapshot
    return y1


if __name__ == '__main__':
    print("Running")
    app.run(debug=True)
