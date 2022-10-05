from datetime import datetime
from dotenv import load_dotenv
import os
import subprocess
import json
import requests

load_dotenv()

api_path = "https://utility-api.jayherron.org"

api_user = os.getenv('API_USER')
api_password = os.getenv('API_PASSWORD')

current_time = datetime.now()

# Measure speed
# This requires the pwrstat cli: https://www.cyberpowersystems.com/product/software/power-panel-personal/powerpanel-for-linux/
# It also requires sudo to run, so this must be added to the sudo cron
command = "pwrstat -status"
output = subprocess.check_output(command, shell=True).decode("utf-8")

for line in output.split("\n"):
    trimmed = line.strip()
    if trimmed.startswith("Utility Voltage"):
        lineArr = trimmed.split(".")
        valStr = lineArr[-1].strip()
        voltage = valStr.split(" ")[0]
    if trimmed.startswith("Load"):
        lineArr = trimmed.split(".")
        valStr = lineArr[-1].strip()
        power = valStr.split(" ")[0]


# Write to SQL
voltage_point_id = "cf04b9ef-6ac8-4e0f-bc5f-9d06e9a1e4f7"
power_point_id = "c9d69b23-adaf-496d-92ab-a61a4cdb5957"

token_request = requests.get(f"{api_path}/auth/token", auth=(api_user, api_password))
assert(token_request.ok)
api_token = token_request.json()["token"]

tokenRequest = requests.post(
    f"{api_path}/his/{voltage_point_id}",
    headers = {"Authorization": f"Bearer {api_token}"},
    data = {
        "ts": f"{current_time}",
        "value": f"{voltage}"
    }
)

tokenRequest = requests.post(
    f"{api_path}/his/{power_point_id}",
    headers = {"Authorization": f"Bearer {api_token}"},
    data = {
        "ts": f"{current_time}",
        "value": f"{power}"
    }
)
