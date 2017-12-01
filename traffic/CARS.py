import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt
import random
#"DIRECT_CAR$$$$"+carID+"$$$$"+qzqueueID+"$$$$"+current+"$$$$command$$$$"+next;
# Set LEDs and sigint handler
# python CARS.py <carID> <QueueId> <Direction>
#python CARS.py 1 0 Right or python CARS.py 1 0 Straight
leds = []
global status
global carID
global queueID
global direction
global grid1
global grid2
moveslp=5
slp=0.4
status="REQ"
if len(sys.argv) == 4:
    carID = sys.argv[1]
    queueID = sys.argv[2]
    direction=sys.argv[3]
else:
    print("usage: CARS.py <carID> <queueID> <direction>")
    sys.exit(1)



#carAction="arrive"+"===="+carName
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

# Instantiate the MQTT client
mqtt_client = paho.Client()

# set up handlers

mqtt_topic = topicname + '/' + socket.gethostname()  # don't change this or you will screw it up for others


def on_connect(client, userdata, flags, rc):
	print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
    global status
    print msg.payload  
    myString = str(msg.payload).split("====")
    # print(myString)

    # print (myString[1])
    if status=="REQ":
        
        if(len(myString)>=4 and myString[1]=='GRANT'):
            # if(carID==myString[2]):
            #     print(carID+"#############"+myString[2])
            # print("**************Permission Granted"+carID+myString[2])
            
            # print len(myString)
            if (len(myString)==4):
                
                # print("I am in right")
                if(carID==myString[2]):
                    status="OUT"
                    goRight(myString[3])
 
            if (len(myString)==5):
                
                # print("I am in straight********************")
                if(carID==myString[2]):
                    status="GRANT"
                    global grid1
                    global grid2
                    grid1 = myString[3]
                    grid2 = myString[4]
                    # print ("I am in straight")

def goStraight():
    global status
    global carID
    global queueID
    global direction
    global grid1
    global grid2
    print "go straight"
    
    #time.sleep(1+int(carID))
    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    messageUI="DIRECT_CAR$$$$"+carID+"$$$$qz"+queueID+"$$$$"+status+"$$$$goForward$$$$qz"+queueID;
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$'+messageUI
    mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    status="qz"+queueID
    # print status
    time.sleep(moveslp)

    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    messageUI="DIRECT_CAR$$$$"+carID+"$$$$qz"+queueID+"$$$$"+status+"$$$$goForward$$$$"+grid1;
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$'+ messageUI
    mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    status=grid1
    # print status
    time.sleep(moveslp)


    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    messageUI="DIRECT_CAR$$$$"+carID+"$$$$qz"+queueID+"$$$$"+status+"$$$$goForward$$$$"+grid2;
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$'+messageUI
    mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    status=grid2
    # print status
    time.sleep(moveslp)


    timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    messageUI="DIRECT_CAR$$$$"+carID+"$$$$qz"+queueID+"$$$$"+status+"$$$$goStraight$$$$"+"exit";
    mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$'+messageUI
    mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    status="EXIT"
    # print status
    time.sleep(slp)


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
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log


# See https://pypi.python.org/pypi/paho-mqtt#option-functions.
mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________'+carID+'\n\n', 0, False)

mqtt_client.connect(broker, '1883')

# You can subscribe to more than one topic: https://pypi.python.org/pypi/paho-mqtt#subscribe-unsubscribe.
# If you do list more than one topic, consdier using message_callback_add for each topic as described above.
# For below, wild-card should do it.
mqtt_client.subscribe(topicname + "/#") #subscribe to all students in class

mqtt_client.loop_start()  # just in case - starts a loop that listens for incoming data and keeps client alive

while True:
    # global status
    # print status
    if(status=="REQ"):
    # print("I am in while loop")
        carAction="REQUEST_ENTRY===="+carID+"===="+queueID+"===="+direction
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # print carAction
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + "===="+carAction
        mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
        time.sleep(5)
    elif(status=="EXIT"):
        carAction="CAR_DONE===="+carID+"===="+queueID
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # print carAction
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + "===="+carAction
        mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
        time.sleep(slp)
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + "===="+carAction
        time.sleep(slp)
        sys.exit(1)
    elif(status=="GRANT"):
        goStraight()

        #just making sure the message was reached
    time.sleep(2)
    # else:
    #     carAction="CAR_ALIVE===="+carID
    #     timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # # print carAction
    #     mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
    #     mqtt_client.publish(mqtt_topic, mqtt_message)  # by doing this publish, we should keep client alive
    #     time.sleep(5)


    
  

  

