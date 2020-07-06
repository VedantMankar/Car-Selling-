from flask import Flask,render_template,redirect,request
import pickle
import jsonify
from sklearn.preprocessing import StandardScaler
import numpy as np 

app = Flask(__name__)

model = pickle.load(open("model.pkl","rb"))
st = StandardScaler()

@app.route('/',methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/predict',methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Years Old'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type = request.form['Fuel_Type']
        if Fuel_Type == "Petrol":
            Fuel_Type = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type=0
            Fuel_Type_Diesel=1
        Seller_Type = request.form['Seller_Type']
        if Seller_Type == 'Individual':
            Seller_Type=1
        else:
            Seller_Type = 0
        Transmission = request.form['Transmission']
        if Transmission == "Manual":
            Transmission = 1
        else:
            Transmission = 0
        prediction = model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type,Seller_Type,Transmission]])
        output = round(prediction[0],2)
        if output < 0:
            return render_template("home.html",prediction_text="Sorry You cannot Sell this Car")
        else:
            return render_template("home.html",prediction_text="You can sell this car at a price of {} Lakhs".format(output))
    else:
        return render_template("home.html")
        

if __name__ == '__main__':
    app.run(debug=True)
