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
def light_riding(carname, status):
    if on_edison == False:
        return
    global leds
#    for led in leds:
 #       led.write(1)
    if carname:
        idx = ord(carname[0])%8
        leds[idx].write(status)

start=False
carName=sys.argv[1]
carAction="arrive"+"===="+carName
def control_c_handler(signum, frame):
#     for led in leds:
#         led.write(1)
    sys.exit()
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    print "Now I am done."
    sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

# Set MQTT stuff
MY_NAME = 'CARS'
broker = 'iot.eclipse.org'
topicname = "cis650prs"
# Public brokers: https://github.com/mqtt/mqtt.github.io/wiki/public_brokers

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
    global start
    global carAction
    print("client")
    print(client)
    print("userdata")
    print(userdata)
    print("msg.topic")
    print(msg.topic)
    print("msg.payload")
    print(msg.payload)
    
    myString = str(msg.payload).split("====")
    print(myString)
    # print (myString[1])
    if(start==False):
     if (len(myString)>1 and myString[1].isdigit()):
       print("Will start cars now")
       start=True

    if (len(myString)>2 and myString[1] == "pickup" and myString[2]==carName):
        print("**************I am in pickup")
        carAction='riding and bonding'+'===='+carName
        # start=True
    #Log all the details for now This can be removed later when not needed
    # if all([msg.topic, msg.payload]):
    #     f = open('CAR.log', 'a')
    #     f.write("\n".join([msg.topic, msg.payload]))
    #     f.close()


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

# Instantiate the MQTT client
mqtt_client = paho.Client()

# set up handlers
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log

mqtt_topic = topicname + '/' + socket.gethostname()  # don't change this or you will screw it up for others

# See https://pypi.python.org/pypi/paho-mqtt#option-functions.
mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)

mqtt_client.connect(broker, '1883')

# You can subscribe to more than one topic: https://pypi.python.org/pypi/paho-mqtt#subscribe-unsubscribe.
# If you do list more than one topic, consdier using message_callback_add for each topic as described above.
# For below, wild-card should do it.
mqtt_client.subscribe(topicname + "/#") #subscribe to all students in class

mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive
cnt=5
while True:
  if start==True:
    # print("I am in while loop")
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # print carAction
    #mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
    #mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    time.sleep(5)
    if ('arrive' in carAction and carName in carAction):
        carAction="waiting"+"===="+carName
        light_riding(carName,1)
        time.sleep(5)

   
    elif (cnt!=0 and 'riding' in carAction and carName in carAction):
        # print("I have come in riding")
        light_riding(carName,0)
        #time.sleep(0.5)
    
    elif(cnt==0 and 'riding' in carAction and carName in carAction):
        carAction="arrive"+"===="+carName
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
        #mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
        carAction="form social group"+"===="+carName
        light_riding(carName,1)
        cnt=5
    cnt-=1
     
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
    mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    time.sleep(3)
  else:
	 print("I am arriving at  turnstile")
	 time.sleep(3)

  

