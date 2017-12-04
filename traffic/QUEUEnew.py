import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt
#"DIRECT_CAR$$$$"+carID+"$$$$"+qzqueueID+"$$$$"+current+"$$$$command$$$$"+next;
# python QUEUE.py 0 1
# Set LEDs and sigint handler
slp = 0.2
leds = []
global subTokenComplete
global meComplete
global isCaptain
global queueID
global grid1
global grid2
global counter
global sendSubtoken
global reqString
global callReqEntryAction
callReqEntryAction = False
sendSubtoken = False
counter = 1
global reqMade #this may change for queue its used to know if lane was requested a car
#request if no lane with subtoken can send done immediately
global subTokenToLane  #parallel lane allowed initialize when you know which queue id you have
global subSubTokenToLane # right lane allowe initialize when you know which queue id you have
isCaptain=False #release when CARS of his and subtoken and subsubtoken he had 
#are done given out are done
isSUBTOKEN=False #to know if lane has subtoken release when that lanes CARS are done
isSUBSUBTOKEN=False #to know if lane has subsubtoken
subTokenComplete=False #for captain to know if CARS of subtoken are done
meComplete=False #to know if cars of captain complete
reqMade=[]
# subTokenToLane=2
if len(sys.argv) == 3:
    queueID = sys.argv[1]
    
    isCaptain=int(sys.argv[2])
else:
    print("usage: QUEUE.py  <queueID> <grid1> <grid2> <isCaptain>")
    sys.exit(1)

#initialize lane related things
if queueID=="0":
    grid1 = "l0"
    grid2 = "l1"
    subTokenToLane="2"
    #subSubTokenToLane="3"

if queueID=="1":
    grid1 = "l1"
    grid2 = "l2"
    subTokenToLane="3"
    #subSubTokenToLane="0"


if queueID=="2":
    grid1 = "l2"
    grid2 = "l3"
    subTokenToLane="0"
    #subSubTokenToLane="1"


if queueID=="3":
    grid1 = "l3"
    grid2 = "l0"
    subTokenToLane="1"
    #subSubTokenToLane="2"
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
MY_NAME = 'QUEUE'
broker = 'iot.eclipse.org'
topicname = "cis650prs2"
# Public brokers: https://github.com/mqtt/mqtt.github.io/wiki/public_brokers

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

# Instantiate the MQTT client
mqtt_client = paho.Client()

mqtt_topic = topicname + '/' + socket.gethostname()  # don't change this or you will screw it up for others


def on_connect(client, userdata, flags, rc):
	print('connected')

# The callback for when a PUBLISH message is received from the server that matches any of your topics.
# However, see note below about message_callback_add.
def on_message(client, userdata, msg):
    global isSUBTOKEN
    print msg.payload
    global subTokenComplete
    global meComplete
    global subTokenToLane
    global reqMade
    global isCaptain
    global reqString
    global callReqEntryAction
    myString = str(msg.payload).split("====")
    # print "##########"
    # print(myString)

    # print (myString[1])

    
    if(len(myString)==3 and myString[1]=='NEXT_CAPTAIN'):
        print("got next captain ****************************************"+queueID)
        if queueID==myString[2]:
            isCaptain=True


    if(len(myString)==4 and myString[1]=='CAR_DONE'):
        if(myString[3]==queueID):
            if isCaptain:
                caridxs = [i for i,x in enumerate(reqMade) if x == int(myString[2])]
                if len(caridxs) > 0:
                    del reqMade[caridxs[0]]
                if len(caridxs) > 1:
                    print("Car got added twice, here's the message: {}".format(myString))
                    sys.exit(1)
                if len(reqMade) == 0:
                    meComplete=True # TODO: Change to send off another car in the queue
            if isSUBTOKEN:
                action="SUBTOKEN_DONE====qz===="+queueID
                timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+action
                mqtt_client.publish(mqtt_topic, mqtt_message)  
                time.sleep(slp)    
    if(len(myString)==4 and myString[1]=='SUBTOKEN_DONE'):
        if(myString[3]==subTokenToLane):
            if isCaptain:
                subTokenComplete=True

            #here code for CAR_DONE of himself and CAR_DONE of 


    if(len(myString)==4 and myString[1]=='SUBTOKEN'):
        print myString[3]
        print queueID
        print "***********"
        if(myString[3]==queueID):
            isSUBTOKEN=True
            print("I got into subtokenssss")
            # Send that you have the subtoken
            msgToUI="SUBTOKEN$$$$"+queueID
            timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
            mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + msgToUI
            mqtt_client.publish(mqtt_topic, mqtt_message)

            print ("subtoken has become true waiting for cars now"+str(isSUBTOKEN))
            if len(reqMade) == 0:
                action="SUBTOKEN_DONE====qz===="+queueID
                timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+action
                mqtt_client.publish(mqtt_topic, mqtt_message) 
                isSUBTOKEN=False  
                time.sleep(slp)
                 #give away the subtoken since no cars   

    if(len(myString)==5 and myString[1]=='REQUEST_ENTRY'):
        print "I am in on_message_Request"
        if(myString[3]==queueID):
            if not int(myString[2]) in reqMade:
                reqMade.append(int(myString[2]))
                reqString = myString
                callReqEntryAction = True
                onReqEntryAction(myString)
          
# You can also add specific callbacks that match specific topics.
# See message_callback_add at https://pypi.python.org/pypi/paho-mqtt#callbacks.
# When you have add ins, then the on_message handler just deals with topics
# you have *not* written an add in for. You can just use the single on_message
# handler for this problem.

def onReqEntryAction(myString):
    global subTokenToLane
    global isSUBTOKEN
    global subTokenComplete
    global meComplete
    global subToken
    global sendSubtoken
    # global reqString
    # myString = reqString
    #pass subtoken to pARALLEL LANE
    print(str(isCaptain)+"iscaptain__")
    print(str(isSUBTOKEN)+"isSUBTOKEN________")
    if(isCaptain):
        # Send that you have the token
        msgToUI="TOKEN$$$$"+queueID
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '$$$$' + msgToUI
        mqtt_client.publish(mqtt_topic, mqtt_message)

    if sendSubtoken:
        laneAction="SUBTOKEN====qz===="+subTokenToLane
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+laneAction
        mqtt_client.publish(mqtt_topic, mqtt_message)
        time.sleep(1.5)
        sendSubtoken = False


        # mark you need to send the subtoken
        #sendSubtoken = True
         
     #   time.sleep(5) # To let Subtoken catch up
        # remove comment when you implement sub_sub_token
        # laneAction="SUB_SUBTOKEN====qz"+subSubTokenToLane
        # timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')

        # mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+laneAction
        # mqtt_client.publish(mqtt_topic, mqtt_message)  
        # time.sleep(3)
    #GRANT CARS THE REQ
    if(isCaptain or isSUBTOKEN):
        #This will have to be looked again when subSubToken
        carAction=""
        global counter
        counter = counter + 1
        if(myString[4]=="Right"):
            print("I am going right________")
            carAction="GRANT===="+myString[2]+"===="+grid1+'===='+str(counter)

        if(myString[4]=="Straight"):
            print("I am going all straight________")
            carAction="GRANT===="+myString[2]+"===="+grid1+"===="+grid2+'===='+str(counter)
        
        print carAction
        #reqMade=True
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
        mqtt_client.publish(mqtt_topic, mqtt_message)  
        time.sleep(slp)
        # time.sleep(counter)

def on_disconnect(client, userdata, rc):
	print("Disconnected in a normal way")
	#graceful so won't send will

def on_log(client, userdata, level, buf):
	pass
	# print("log: {}".format(buf)) # only semi-useful IMHO

# set up handlers
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_log = on_log


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
    if cnt % 50 == 0:
        carAction="QUEUE_ALIVE===="+queueID
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
        mqtt_client.publish(mqtt_topic, mqtt_message)  
        time.sleep(slp)
        cnt = cnt + 1

#     if sendSubtoken:    
#         laneAction="SUBTOKEN====qz===="+subTokenToLane
#         timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
#         mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+laneAction
#         mqtt_client.publish(mqtt_topic, mqtt_message)
#         time.sleep(1.5)
#         sendSubtoken = False

    # if callReqEntryAction:
    #     onReqEntryAction()
    #     callReqEntryAction = False

    if(subTokenComplete and meComplete):
        #pass token to next
        print "pass to next leader"
        nextCaptain=(int(queueID)+1)%4
        carAction="NEXT_CAPTAIN===="+str(nextCaptain)
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    # print carAction
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '===='+carAction
        mqtt_client.publish(mqtt_topic, mqtt_message)  
        time.sleep(slp)

        subTokenComplete=False
        meComplete=False
        isCaptain=False
        counter = 1

