from flask import Flask, request, jsonify
from task_processor import TaskProcessor, setup_google_sheets
from clickup_client import ClickUpClient
from cbr_system import CBRSystem
import os
import json

app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

with open('access_token.txt', 'r') as f:
    ACCESS_TOKEN = f.read().strip()

clickup_client = ClickUpClient(access_token=ACCESS_TOKEN, folder_id=config['folder_id'])
google_sheets_client = setup_google_sheets(config['google_credentials'])
cbr_system = CBRSystem(google_sheets_client)
task_processor = TaskProcessor(clickup_client, cbr_system)

@app.route('/new_task', methods=['POST'])
def new_task():
    data = request.json
    task_processor.process_task(data)
    return jsonify({"status": "processed"})

@app.route('/update_task', methods=['POST'])
def update_task():
    data = request.json
    task_processor.process_task(data)
    return jsonify({"status": "processed"})

if __name__ == '__main__':
    app.run(debug=True)
