import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
import random
from datetime import datetime as dt
#timestamp||||FLUENT||||CZ||||CZ0Count||||CZ1count||||CZ2Count||||CZ3Count
#timestamp||||FLUENT||||SUBTOKEN||||IDWHOHASSUBTOKEN

# Set state variables
# Possible states: in_contention, no_contention, leader, no_contention_and_elected
# in_contention means you might be the leader
# no_contention means you received a ID that's higer than yours
# XXX: Maybe want to split up later?
# Gonna have to expand this to also account for timeout
global mqtt_client
global mqtt_topic

# Set LEDs and sigint handler
leds = []
try:
    import mraa
except ImportError:
    on_edison = False
else: 
    on_edison = True
    # Initialize lights
    for i in range(2,10):
        led = mraa.Gpio(i)
        led.dir(mraa.DIR_OUT)
        leds.append(led)
        time.sleep(0.1)
        led.write(1)

def turnOn(light):
    if on_edison ==True:
        leds[int(light)].write(0)
    else:
        print("Turned on {}".format(light))
def turnOff(light):
    if on_edison ==True:
        leds[int(light)].write(1)

def control_c_handler(signum, frame):
    sys.exit()
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    for i in range(8):
        turnOff(i)
    print("Now I am done.")
    sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

# Set MQTT stuff
MY_NAME = 'token_checker'
broker = 'iot.eclipse.org'
topicname = "cis650prs"

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

def on_connect(client, userdata, flags, rc):
    print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
# Message is of the form
# timestamp||||FLUENT||||TOKEN||||IDWHOHASTOKEN
def on_message(client, userdata, msg):
    myList = str(msg.payload).split("||||")
    if len(myList) == 4 and myList[1] == 'FLUENT' and myList[2] == 'TOKEN':
        for i in range(8):
            turnOff(i)
        turnOn(int(myList[3]))

# You can also add specific callbacks that match specific topics.
# See message_callback_add at https://pypi.python.org/pypi/paho-mqtt#callbacks.
# When you have add ins, then the on_message handler just deals with topics
# you have *not* written an add in for. You can just use the single on_message
# handler for this problem.

def on_disconnect(client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will

def on_log(client, userdata, level, buf):
    pass
    # print("log: {}".format(buf)) # only semi-useful IMHO

def main():
    global mqtt_client
    global mqtt_topic
    # Instantiate the MQTT client
    mqtt_client = paho.Client()

    # set up handlers
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_log = on_log

    mqtt_topic = topicname + '/' + socket.gethostname()

    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, '1883')
    mqtt_client.subscribe(topicname + "/#") #subscribe to all students in class
    mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive
    while True:
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        msg_start = "[%s] %s " % (timestamp,ip_addr)
        mqtt_message =  msg_start + '====fluent keepalive'
        mqtt_client.publish(mqtt_topic, mqtt_message)
        time.sleep(5) # This is the timeout

if __name__ == '__main__':
    main()
