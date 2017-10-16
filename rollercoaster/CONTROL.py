import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

# Set LEDs and sigint handler
# import mraa
# leds = []
# for i in range(2,10):
#   led = mraa.Gpio(i)
#   led.dir(mraa.DIR_OUT)
#   leds.append(led)
#   time.sleep(0.05)
#   led.write(1)

passenger_total = 0
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
MY_NAME = 'CONTROL'
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

#For now, when you get a message print it
def on_message(client, userdata, msg):
	
        print("client")
        print(client)
	print("userdata")
	print(userdata)
	print("msg.topic")
	print(msg.topic)
	print("msg.payload")
	
        print(msg.payload)
        read = open('output.txt','r')
        append = open('output.txt', 'a+')
        ## To do, save message to file
        try:
            myString = str(msg.payload).split("====")
            if (myString[1] == "Passenger"):
                passenger_total = passenger_total + 1
                #TODO: Turn Led on, ensure they are on per passenger
                try:
                    append.write(str(myString[1]) + "\n")
                except:
                    print("Error writting  message to file")
        except:
            print("Error in message")
            pass
        read.close()
        append.close()

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

people_on_platform =0

while True:
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    if (passenger_total == 3)
        #TODO: Turn off all 3 led lights, 
        #TODO: Send notice to car we are ready to leave
        #TODO: Same notice to car, used for turnstile, to notify platform has room
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '==== '+ "3"
        mqtt_client.publish(mqtt_topic, mqtt_message)  
    else:
        #TODO: Need to send a message we are not ready yet
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '==== '+ str(passenger_total)
        mqtt_client.publish(mqtt_topic, mqtt_message)  

    time.sleep(5)

# I have the loop_stop() in the control_c_handler above. A bit kludgey.
