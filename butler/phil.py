import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

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
    print("Received" + ", ".join([msg.topic, msg.payload + "\n"]))

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
    state = "req sitdown"
    if len(sys.argv) == 4:
        philname = sys.argv[1]
        leftfork = sys.argv[2]
        rightfork = sys.argv[3]
    else:
        print("usage: phil.py <name> <leftfork> <rightfork>")
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
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '====' + philname + ' l:' + leftfork + ' r:' + rightfork
        mqtt_client.publish(mqtt_topic, mqtt_message) # by doing this publish, we should keep client alive
        time.sleep(3)

if __name__ == '__main__':
    main()
