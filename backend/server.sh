#!/bin/bash
# Start the carbon dashboard server

export SUBSCRIPTION_ID="59d64684-e7c9-4397-8982-6b775a473b74"
python3 -m venv venv     
source venv/bin/activate    
python3 -m pip install -r requirements.txt
flask --app carbon_dashboard_api run 