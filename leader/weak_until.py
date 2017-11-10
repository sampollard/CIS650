# Checks for the assert statement
#     !<l> W <r>
# where l and r are some messages which can be sent in this protocol.
# Both <l> and <r> fluents start out false.
# For the assignment, do
# python weak_until.py leader====0 election====0

#Message if Cheater: $$$$W$$$$0$$$$Cheater
#Message if OK: $$$$W$$$$0$$$$OK

#left arg Message to show in GUI $$$$lw$$$$0$$$$leader====0

# right arg arg Message to show in GUI $$$$rw$$$$0$$$$election====0


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
# These are global too but we know how to initialize them
failed = False # This will only change to True once.
rb = False
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
MY_NAME = 'weak_until'
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
def on_message(client, userdata, msg):
    global rb
    global lb
    global failed

    # msg.payload is bytes, msg.topic is string. That's stupid.
    print("Received " + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
    myString = str(msg.payload).split("====")
    print myString

    if(len(myString)>3):
        print myString[2]
        print myString[3]
        temp=myString[2]+"===="+myString[3]
        print temp
        
        if temp == l:
            print("Matched {}".format(l))
            lb = True
        elif temp == r:
            print("Matched {}".format(r)) # TODO: GUI it
            rb = True
        if lb == True and rb == False:
            print("Assert (!{} W {}) failed".format(l, r)) # TODO: GUI it
            failed = True
            # sys.exit(1)
def on_disconnect(client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will

def on_log(client, userdata, level, buf):
    pass
    # print("log: {}".format(buf)) # only semi-useful IMHO

def main():
    global l
    global r
    if len(sys.argv) == 3:
        l = sys.argv[1]
        r = sys.argv[2]
    else:
        print("usage: weak_until.py <l> <r> where we track (!<l> W <r>)")
        sys.exit(1)
    # Instantiate the MQTT client
    mqtt_client = paho.Client()
    myString = l.split("====")
    clientNo=myString[1]
    # set up handlers
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_log = on_log

    mqtt_topic = topicname + '/' + socket.gethostname()

    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, 1883)
    mqtt_client.subscribe(topicname + "/#") #subscribe to all students in class
    mqtt_client.loop_start() # just in case - starts a loop that listens for incoming data and keeps client alive
    # Send the <l> message for the GUI
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'lw'+'$$$$'+clientNo+ '$$$$' + l
    mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
    # Send the <r> message for the GUI
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'rw'+'$$$$'+clientNo + '$$$$' + r
    mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
    while True:
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        if failed:
            mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'W' +'$$$$'+clientNo+ '$$$$' + 'Cheater'
        else:
            mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + 'W' +'$$$$'+clientNo+ '$$$$' + 'OK'
        mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
        time.sleep(4)

if __name__ == '__main__':
    main()
