import imp
from webbrowser import get
from flask import Flask, redirect, render_template, request, url_for
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_car_price_prediction.pkl','rb'))
@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')
standard_to = StandardScaler()
@app.route("/predict", methods = ['Post'])
def predict():
    if request.method == 'POST':
        year = int(request.form['Year'])
        km_driven = int(request.form['KM_Drive'])
        present_price = float(request.form['present_price'])
        owner = int(request.form['owners'])
        if(request.form['fuel']=='Petrol'):
             petrol = 1
             diesel = 0
        elif(request.form['fuel']=='Diesel'):
            petrol = 0
            diesel = 1
        if(request.form['transmission']=='Manual'):
            manual = 1
        else:
            manual = 0
        if(request.form['Seller_Type_Individual']=='Individual'):
            individual = 1
        else:
            individual = 0
        no_of_years = 2022-year
        prediction = model.predict([[present_price,km_driven,owner,no_of_years,diesel,petrol,individual,manual]])
        output = round(prediction[0],2)
        if output < 0:

            return render_template('predict.html', prediction_texts = "sorry your car cannot sell")
           
        else:

            return render_template('predict.html', prediction_texts = "you can sell this car at {} ".format(output))
            
    else:
        return render_template('index.html',prediction_texts = 'Sorry')   
        
    

if __name__=='__main__':
    app.run(debug=True)
