import paho.mqtt.client as mqtt
import random
import time

# MQTT broker details
broker_address = "broker.hivemq.com"
broker_port = 1883

# Initialize the bulb state and brightness level
bulb_state = False
brightness_level = 0

# The callback function to execute when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribe to the smart-light-bulb/state topic
    client.subscribe("smart-light-bulb/state")

# The callback function to execute when the client receives a message from the server
def on_message(client, userdata, msg):
    global bulb_state, brightness_level
    if msg.topic == "smart-light-bulb/state":
        bulb_state = msg.payload.decode() == "True"
    elif msg.topic == "smart-light-bulb/brightness":
        brightness_level = int(msg.payload.decode())

# Create a client instance and connect to the broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)

# The main loop that runs continuously
def loop():
    global bulb_state, brightness_level
    while True:
        # Randomly change the bulb state and brightness level
        bulb_state = random.choice([True, False])
        brightness_level = random.randint(0, 100)

        # Publish the current bulb state and brightness level
        client.publish("smart-light-bulb/state", str(bulb_state))
        if bulb_state:
            client.publish("smart-light-bulb/brightness", str(brightness_level))

        # Print the current state and brightness level
        if bulb_state:
            print("The bulb is on with brightness level: {}".format(brightness_level))
        else:
            print("The bulb is off")
        
        time.sleep(1)

# Start the main loop
loop()
