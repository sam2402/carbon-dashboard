#!/bin/bash
# Start the carbon dashboard server

export SUBSCRIPTION_ID="59d64684-e7c9-4397-8982-6b775a473b74"
export ELECTRICITY_MAPPER_TOKEN="fake_key"
export FLASK_APP=carbon_dashboard_api.py
python3 -m venv venv     
source venv/bin/activate    
python3 -m pip install -r requirements.txt
flask --app carbon_dashboard_api run