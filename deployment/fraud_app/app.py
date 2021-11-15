#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: msabry
"""


from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from utils import *


LOGGER = init_logger()

app = Flask(__name__)

clf = get_clf()
scaler = get_scaler()


@app.route("/")
def hello():
    return "THIS IS A FRAUD DETECTION APPLICATION"

@app.route('/is-fraud', methods=['POST'])
def predict_transaction():
    if request.method == 'POST':
        db_engine = create_engine('postgresql://postgres:password@FD_postgres:5432/frauddb')

        transaction = request.get_json()
        
        with db_engine.connect() as connection:
            transaction_check = check_transaction(transaction, connection)
        
            if transaction_check == "Fraud":
               transaction_prediction = True
        
            else:  
                transaction_prediction = predict(scaler, clf, transaction)
        
            register_transaction(transaction, connection, transaction_prediction)
        
            transaction_status = {"isFraud":transaction_prediction}
        
        return jsonify(transaction_status)
    else:
        return "Invalid Method"



if __name__=="__main__":
    app.run(host = "0.0.0.0", port="5000")













