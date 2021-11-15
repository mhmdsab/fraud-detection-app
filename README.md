# fraud-detection-app
Fraud Detection System For Tracking Fraud Transactions

This repository can be split into two parts:

  1 - Model Development:

      This part consists of two notebooks:
      
        a - EDA.ipynb which includes basic EDA about the data, which is a good start point 
            for feature engineering.
        
        b - Train.ipynb which contains feature engineering and model training script.
      
      The model used to solve this problem is random forest. It acheived high accuracy 
      very close to 100% for precision, recall and f1-score.
      
  2 - Model Deployment:
  
      This is the complementary part of the system, model is deployed to serve at high scale. 
      The deployment architecture is as follows:
      
        1 - fraud-service which predicts whether a transaction is fraud or not.
        
        2 - nginx server which works as a load balancer among fraud service multiple instances.
        
        3 - postgresql database to record any transaction, this database is used to track the history of 
            the transactions performed per user.
        
        4 - pgadmin service to monitor the database records.
        
     The stack is deployed via docker swarm with 4 replicas for nginx server and 2 replicas for fraud-service. 
     

Before running training notebooks, create a folder with name Data and place the csv file at https://drive.google.com/file/d/1JKMiKwDAeAaETNhmwvOyJ_WoDagYRP3n/view inside it.


