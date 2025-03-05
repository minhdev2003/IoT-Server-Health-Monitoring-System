import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "rule28.i4t.swin.edu.au"
port = 1883
username = "<103496945>"  
password = username  

# Topics to subscribe to
private_topic = f"{username}/server_health/#"
public_topic = "public/#"

def check_metrics(data_str):
#Analyzes the received metrics data and checks for concerning values

    try:
        # Convert the string representation of dictionary back to a dictionary
        data = eval(data_str)
        
        # Check for threshold violations
        # CPU usage above 90% is considered critical
        if data['cpu_usage'] > 90:
            print(f"WARNING: High CPU usage detected: {data['cpu_usage']}%")
        
        # RAM usage above 90% is considered critical    
        if data['ram_usage_percent'] > 90:
            print(f"WARNING: High RAM usage detected: {data['ram_usage_percent']}%")
            
    except Exception as e:
        print(f"Error processing metrics: {e}")

def on_connect(client, userdata, flags, rc):
#    Callback function that runs when the client connects to the MQTT broker

    if rc == 0:
        print("Connected successfully to MQTT broker")
        # Subscribe to both private and public topics
        # QoS level 0 means "at most once" delivery
        client.subscribe([(private_topic, 0), (public_topic, 0)])
        print(f"Subscribed to {private_topic} and {public_topic}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    #Callback function that runs when a message is received from the broker

    try:
        # Print received message details with clear formatting
        print("\n--- New Message ---")
        print(f"Topic: {msg.topic}")              # The topic this message was published to
        print(f"Data: {msg.payload.decode()}")    # The actual message data, decoded from bytes
        
        # If message is from server health metrics topic, analyze it
        if 'server_health/metrics' in msg.topic:
            check_metrics(msg.payload.decode())
            
    except Exception as e:
        print(f"Error processing message: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Set up authentication credentials
client.username_pw_set(username, password)

# Assign callback functions
client.on_connect = on_connect    # Called when client connects/attempts to connect
client.on_message = on_message    # Called when message is received

# Attempt to connect to the MQTT broker
try:
    print(f"Attempting to connect to {broker_address}:{port}")
    client.connect(broker_address, port)
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# Startup messages
print("Starting the monitoring system. Press Ctrl+C to stop.")
print("Waiting for server health metrics...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    # Handle clean shutdown when Ctrl+C is pressed
    print("\nStopping the monitoring system...")
    client.disconnect()