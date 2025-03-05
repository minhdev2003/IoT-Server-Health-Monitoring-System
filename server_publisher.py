import paho.mqtt.client as mqtt
import time
import random

# MQTT broker details
broker_address = "rule28.i4t.swin.edu.au"
port = 1883
username = "<103496945>"  
password = username

# Topic to publish to
topic = f"{username}/server_health/metrics"

# Callback function for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")

# Create a client instance
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect

# Connect to the broker
try:
    print(f"Attempting to connect to {broker_address}:{port}")
    client.connect(broker_address, port)
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# Start the loop
client.loop_start()

def generate_server_metrics():
    cpu_usage = round(random.uniform(20, 95), 2)  
    ram_total = 16384  # Simulating 16GB total RAM
    ram_used = round(random.uniform(4096, 14000), 2)  
    ram_percent = round((ram_used / ram_total) * 100, 2)
    
    # Create a structured message
    metrics = {
        "cpu_usage": cpu_usage,
        "ram_total_mb": ram_total,
        "ram_used_mb": ram_used,
        "ram_usage_percent": ram_percent,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return str(metrics)

try:
    print("Server Health Monitor Started")
    print("Publishing metrics every 5 seconds...")
    while True:
        data = generate_server_metrics()
        result = client.publish(topic, data)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Published: {data}")
        else:
            print(f"Failed to publish message. Error code: {result.rc}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopping the server monitor...")
    client.loop_stop()
    client.disconnect()