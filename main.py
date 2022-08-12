from datetime import datetime
from dotenv import load_dotenv
import os
import subprocess
import json
import psycopg2

load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

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

conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

cur.execute("INSERT INTO his (\"pointId\", ts, value) VALUES (%s, %s, %s)", (voltage_point_id, current_time, voltage))
cur.execute("INSERT INTO his (\"pointId\", ts, value) VALUES (%s, %s, %s)", (power_point_id, current_time, power))

conn.commit()
cur.close()
conn.close()
