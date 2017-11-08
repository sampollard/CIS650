import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

# Set LEDs and sigint handler
leds = []
lookUpLight = {'a':0,'b':1,'c':2, 'd':3, 'e' :4,'f':5,'g':6}
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
        if on_edison==True:
            leds[lookUpLight[light]].write(0)
        else:
            print("Simulate light on")
def turnOff(light):
        if on_edison==True:
            leds[lookUpLight[light]].write(1)
        else:
            print("Simulate light off")

def set_light(idx, value=1): # By default, on
    if on_edison == False:
        return
    global leds
    leds[idx].write(status)

def control_c_handler(signum, frame):
    sys.exit()
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    print "Now I am done."
    sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

#start=False
forkName=sys.argv[1]
inUse=False
forkAction="in_use"+"===="+forkName

# Set MQTT stuff
MY_NAME = 'fork'
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
    global forkName
    global inUse
    global forkAction
    print("Received" + ", ".join([msg.topic, msg.payload + "\n"]))
    myString = str(msg.payload).split("====")
    print(myString)
    if (len(myString)==4 and myString[2] == "req_fork" and myString[3]==forkName):
        if(inUse == False):
            #turnOn(forkName)
            forkAction=myString[1]+"===="+"fork_granted"+"===="+forkName
            inUse=True
        else:
            print(forkName+"  in use  wait")
            #forkAction="in_use"+"===="+forkName+"===="+inUse
    if (len(myString)==4 and myString[2] == "put_down" and myString[3]==forkName):
        inUse=False
        turnOff(forkName)
        print(forkName+"  done")
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
    global forkAction
    global forkName
    if len(sys.argv) > 1:
        forknum = sys.argv[1]
    else:
        print("usage: fork.py <int>")
        sys.exit(1)
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
        if 'granted' in forkAction and forkName in forkAction: 
            turnOn(forkName)
	    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+forkAction
            mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
            forkAction=forkName+ " in use"
        # if inUse:
        #     mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+'waiting'
        #     mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
        time.sleep(2)

if __name__ == '__main__':
    main()
