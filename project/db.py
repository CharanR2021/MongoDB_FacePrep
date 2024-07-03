from pymongo import MongoClient
import streamlit as st
import os
import json
from langchain_core.output_parsers import StrOutputParser
import time
from datetime import timedelta
import pandas as pd
from datetime import datetime


client = MongoClient('mongodb://localhost:27017/')
db = client['orders_db']  #database name
dbc = db['orders']  # Collection

sample_order = {
    'User_ID': 2,
    'Order_ID': 100001,
    'Order_Name': 'Sample Order 1',
    'Description': 'Sample description for order 1',
    'Order_date': datetime.strptime('2023-06-15', '%Y-%m-%d'),
    'Delivery_Date': datetime.strptime('2023-07-01', '%Y-%m-%d'),
    'Status': 'Pending',
    'TransitionFrom': 'Warehouse',
    'TransitionTo': 'Dispatch',
    'TransitionDate': datetime.strptime('2023-06-30', '%Y-%m-%d')
}

# Insert the sample data into MongoDB
result = dbc.insert_one(sample_order)
print(f"Inserted order with ID: {result.inserted_id}")