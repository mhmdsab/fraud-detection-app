#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: msabry
"""

import pickle
import numpy as np
from logging import getLogger, INFO, FileHandler,  Formatter,  StreamHandler

transaction_type_dict = {"PAYMENT":0,
                        "TRANSFER":1,
                        "CASH_OUT":2,
                        "DEBIT":3,
                        "CASH_IN":4}

def init_logger(log_file='Fraud.log'):
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    handler1 = StreamHandler()
    handler1.setFormatter(Formatter("%(message)s"))
    handler2 = FileHandler(filename=log_file)
    handler2.setFormatter(Formatter("%(message)s"))
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    return logger


def get_balance_diff(old_balance, new_balance):
    return new_balance-old_balance

def balance_equals_amount(old_balance, amount):
    return (old_balance==amount) * 1


def get_clf():
    with open('classifier.pickle', "rb") as f:
        clf = pickle.load(f)
    return clf

def get_scaler():
    with open('scaler.pickle', "rb") as f:
        scaler = pickle.load(f)
    return scaler

def predict(scaler, clf, req):
    amount = scaler.transform([[req["amount"]]])
    oldbalanceOrig = scaler.transform([[req["oldbalanceOrig"]]])
    newbalanceOrig = scaler.transform([[req["newbalanceOrig"]]])
    oldbalanceDest = scaler.transform([[req["oldbalanceDest"]]])
    newbalanceDest = scaler.transform([[req["newbalanceDest"]]])
    orig_diff = get_balance_diff(oldbalanceOrig, newbalanceOrig)
    dest_diff = get_balance_diff(oldbalanceDest, newbalanceDest)
    step =  np.array([[req["step"]]])
    type_ = np.array([[transaction_type_dict[req["type"]]]])
    balance_equals_amnt = balance_equals_amount(oldbalanceOrig, amount)
    X = np.concatenate((amount, oldbalanceOrig, newbalanceOrig, oldbalanceDest, newbalanceDest,
                      orig_diff, dest_diff, step, type_, balance_equals_amnt), axis = -1)
    prediction = clf.predict(X)[0]

    if prediction ==1:
        return True
    else:
        return False


def check_transaction(req, connection):
    nameOrig = req["nameOrig"]
    step = req["step"]
    transactions = connection.execute(f"SELECT * FROM transactions WHERE nameorig='{nameOrig}' AND step={step}").fetchall()
    if len(transactions)>=4:
        return "Fraud"
    else:
        return "Not Fraud"



def register_transaction(req, connection, transaction_prediction):
    step = req["step"]
    type_ = req["type"]
    nameOrig = req["nameOrig"]
    nameDest = req["nameDest"]
    amount = req["amount"]
    oldbalanceOrig = req["oldbalanceOrig"]
    newbalanceOrig = req["newbalanceOrig"]
    oldbalanceDest = req["oldbalanceDest"]
    newbalanceDest = req["newbalanceDest"]
    
    registeration = connection.execute(f'''INSERT INTO transactions (step, type, amount, nameorig, oldbalanceorig, 
                                                                 newbalanceorig, namedest, oldbalancedest, newbalancedest, 
                                                                 isfraud)
                                       VALUES ({step}, '{type_}', {amount}, '{nameOrig}', {oldbalanceOrig}, {newbalanceOrig}, 
                                               '{nameDest}', {oldbalanceDest}, {newbalanceDest}, {transaction_prediction*1})''')




















    
    