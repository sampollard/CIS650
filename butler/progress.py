# Checks for the progress statement
#     <l> --> <r>
# where l and r are some messages which can be sent in this protocol.

import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

# TODO: Initialize GUI

global l
global r
rb = False # These are global too but we know how to initialize them
lb = False

def control_c_handler(signum, frame):
    sys.exit()
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    print("Now I am done.")
    sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

# Set MQTT stuff
MY_NAME = 'progress'
broker = 'iot.eclipse.org'
topicname = "cis650prs"

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

mqtt_client = paho.Client()
mqtt_topic = topicname + '/' + socket.gethostname()
def on_connect(client, userdata, flags, rc):
    print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
    global rb
    global lb
    global mqtt_client
    global mqtt_topic
    # msg.payload is bytes, msg.topic is string. That's stupid.
    print("**********Received " + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
    myString = str(msg.payload).split("====")
    # print "====".join(myString[1:])
    if "====".join(myString[1:]) == l:

        print("Matched {}".format(l)) # TODO: GUI it
        lb = True
    elif "====".join(myString[1:]) == r:
        print("Matched {}".format(r)) # TODO: GUI it
        rb = True
        if lb == True and rb == True:
           print("*********Progress (!{} -->{}) failed".format(l, r)) # TODO: GUI it
           timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
           mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'P'+'$$$$'+'Failed'
           mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
           time.sleep(5)
           print("Progress Failed thus exiting.")
           sys.exit(0)
           lb=False
           rb=False
def on_disconnect(client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will

def on_log(client, userdata, level, buf):
    pass
    # print("log: {}".format(buf)) # only semi-useful IMHO

    # set up handlers
    

def main():
    global l
    global r
    global mqtt_client
    global mqtt_topic
    if len(sys.argv) == 3:
        l = sys.argv[1]
        r = sys.argv[2]
    else:
        print("usage: progress.py <l> <r> where we track (<l> --> <r>)")
        sys.exit(1)

    

    # Instantiate the MQTT client
    # mqtt_client = paho.Client()

    # set up handlers
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_log = on_log
    print ("wtf is happening")
    

    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, 1883)
    mqtt_client.subscribe(topicname + "/#") #subscribe to all students in class
    mqtt_client.loop_start() # just in case - starts a loop that listens for incoming data and keeps client alive
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'lp'+'$$$$'+l
    mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
    time.sleep(2)
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'rp'+'$$$$'+r
    mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
    time.sleep(2)

    while True:
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'P'+'$$$$'+'OK'
        mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
        time.sleep(8)

if __name__ == '__main__':
    main()
