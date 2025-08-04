import csv
import requests
import time
timestamp = int(time.time()) - 3600  # 1 hour ago

# InfluxDB settings
INFLUX_URL = "http://localhost:8086/write?db=tests"
AUTH = ("admin", "admin123")

def push_metrics(csv_file):
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test = row["test"]
            duration = row["duration"]
            status = row["status"]
            # Convert status to binary
            status_val = "1" if status.upper() == "PASS" else "0"
            # Build line protocol
            line = f"test_results,test={test} status={status_val},duration={duration} {timestamp}000000000"
            # Send to InfluxDB
            response = requests.post(INFLUX_URL, data=line, auth=AUTH)
            if response.status_code != 204:
                print("Error:", response.text)

if __name__ == "__main__":
    push_metrics("example_test_data.csv")
    print("Metrics pushed successfully.")
