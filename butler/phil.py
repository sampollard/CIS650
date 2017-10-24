import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

# Set state variables
state = "req_sitdown" # global state variable
if len(sys.argv) == 4:
    philname = sys.argv[1]
    leftfork = sys.argv[2]
    rightfork = sys.argv[3]
else:
    print("usage: phil.py <name> <leftfork> <rightfork>")
    sys.exit(1)

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
    global state
    print("Received " + ", ".join([msg.topic, msg.payload + "\n"]))
    mlist = str(msg.payload).split("====")
    if state == 'req_sitdown':
        if len(mlist) == 3 and (
                mlist[1] == philname and
                mlist[2] == 'sitdown_granted'):
            state = 'sitdown'
    elif state == 'req_left_fork':
        if len(mlist) == 4 and (
                mlist[1] == philname and
                mlist[2] == 'fork_granted' and
                mlist[3] == leftfork):
            print("got fork " + leftfork)
            state = 'req_right_fork'
    elif state == 'req_right_fork':
        if len(mlist) == 4 and (
                mlist[1] == philname and
                mlist[2] == 'fork_granted' and
                mlist[3] == rightfork):
            print("got fork " + rightfork)
            state = 'eat'

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
    # possible states:
    # 'req_sitdown', 'sitdown', 'req_left_fork', 'req_right_fork', (both just send 0=req_fork=a)
    # 'eat', 'put down left fork', 'put down right fork',
    # 'leave' (then go back to  'req sitdown')
    global state
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
        global state
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        msg_start = "[%s] %s " % (timestamp,ip_addr)
        if state == 'req_sitdown':
            mqtt_message =  msg_start + '====' + philname + '====req_sitdown'
            mqtt_client.publish(mqtt_topic, mqtt_message)
        elif state == 'sitdown':
            print(philname + " sits down")
            time.sleep(2)
            state = 'req_left_fork'
        elif state == 'req_left_fork':
            mqtt_message =  msg_start + '====' + philname + '====req_fork====' + leftfork
            mqtt_client.publish(mqtt_topic, mqtt_message)
        elif state == 'req_right_fork':
            mqtt_message =  msg_start + '====' + philname + '====req_fork====' + rightfork
            mqtt_client.publish(mqtt_topic, mqtt_message)
        elif state == 'eat':
            print(philname + " is eating")
            time.sleep(2)
            state = 'put_down_left_fork'
        elif state == 'put_down_left_fork':
            mqtt_message =  msg_start + '====' + philname + '====put_down====' + leftfork
            mqtt_client.publish(mqtt_topic, mqtt_message)
            state = 'put_down_right_fork'
        elif state == 'put_down_right_fork':
            mqtt_message =  msg_start + '====' + philname + '====put_down====' + rightfork
            mqtt_client.publish(mqtt_topic, mqtt_message)
            time.sleep(2)
            mqtt_message =  msg_start + '====' + philname + '====leave'
            mqtt_client.publish(mqtt_topic, mqtt_message)
            state = 'req_sitdown'
        else:
            print("Error, you should never be in state " + state)
            return
        time.sleep(2)

if __name__ == '__main__':
    main()
