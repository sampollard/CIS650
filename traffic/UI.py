#Notes

#TODO Adding three asserts to UI
# Adding three weak untills`
# !leader0 untill election0
# ts ==== DEST (id) ==== leader ==== 0
# So if 0 is the cheater, then 1 would catch it right away
#

import sys, os
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import * #import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PIL import Image
from PIL.ImageQt import ImageQt
import socket
import paho.mqtt.client as paho
import signal
import time
import os
import sys
from datetime import datetime as dt

def control_c_handler(signum, frame):
    sys.exit()
    print('saw control-c')
    mqtt_client.disconnect()
    mqtt_client.loop_stop()  # waits until DISCONNECT message is sent out
    print("Now I am done.")
    sys.exit(0)
signal.signal(signal.SIGINT, control_c_handler)

# Set MQTT stuff
MY_NAME = 'UI model checker'
broker = 'iot.eclipse.org'
topicname = "cis650prs"

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()

# Set up mqtt on_* functions that don't change the GUI
def on_disconnect(self, client, userdata, rc):
    print("Disconnected in a normal way")
    #graceful so won't send will
def on_log(self, _userdata, level, buf):
    pass
def on_message(client, userdata, msg):
    print("Received " + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))

class mainClass(QWidget):
    client_handler = QtCore.pyqtSignal(object)

    #Global car messages to update
    countCZ0 = 0
    countCZ1 = 0
    countCZ2 = 0
    countCZ3 = 0
    g_car0 = "????"
    g_car1 = "????"
    g_car2 = "????"
    g_car3 = "????"
    #token = "No one"
    #sub_token = "No one"
    messageQueue = []

    # Start out true, only can turn to False once
    #No weak untills yet
 
    def __init__(self, mqtt_client,mqtt_topic):
        super().__init__()
        self._mqtt_client = mqtt_client
        self._mqtt_topic = mqtt_topic
        self.initUI()

    def initUI(self): 
        #This is the layout
        layout = QVBoxLayout(self)
        #Add the two layouts for the scroll boxes

        layout.setContentsMargins(10, 0, 10, 600)
        layout.setSpacing(0)
        layout.insertStretch(0,0);
        #Intro message
        self.introductionText = QLabel(" Welcome to our program\n\n")
        self.introductionText.setAlignment(Qt.AlignCenter) 
        #Add text to layout
        layout.addWidget(self.introductionText)

        #Line spce
        self.lineSpace0 = QLabel()
        self.lineBreak0=QLabel()
        self.lineBreak1=QLabel()
        self.lineBreak2=QLabel()
        self.lineBreak3=QLabel()
        self.lineBreak4=QLabel()
        
        self.sub_tokenLine=QLabel()
        self.tokenLine=QLabel()
        self.tokenLine.setText("No One")       
        self.sub_tokenLine.setText("No One")

        self.lineBreak0.setText("---------------------------------------------------------------------------")       
        self.lineBreak1.setText("---------------------------------------------------------------------------")       
        self.lineBreak2.setText("---------------------------------------------------------------------------")       
        self.lineBreak3.setText("---------------------------------------------------------------------------")       
        self.lineBreak4.setText("---------------------------------------------------------------------------")       

        #Add different labels 
        self.title = QLabel()
        
        
        self.car0= QLabel()
        self.car1= QLabel()
        self.car2= QLabel()
        self.car3= QLabel()
        self.car4= QLabel()
        self.car5= QLabel()
        self.car6= QLabel()

        #+carID+"$$$$"+qzqueueID+"$$$$"+current+"$$$$command$$$$"+next 
        self.title.setText("  Car     qzqueueID    Current          command       next") 
        self.car0.setText( "   waiting               ")
        self.car1.setText( "   waiting              ")
        self.car2.setText( "   waiting               ")
        self.car3.setText( "   waiting               ")
        self.car4.setText( "   waiting               ")
        self.car5.setText( "   waiting               ")
        self.car6.setText( "   waiting               ")
        
     
	
        self.title.setAlignment(Qt.AlignCenter)
        self.car0.setAlignment(Qt.AlignCenter)
        self.car1.setAlignment(Qt.AlignCenter)
        self.car2.setAlignment(Qt.AlignCenter)
        self.car3.setAlignment(Qt.AlignCenter)
        self.car4.setAlignment(Qt.AlignCenter)
        self.car5.setAlignment(Qt.AlignCenter)
        self.car6.setAlignment(Qt.AlignCenter)

        
        self.tokenLine.setAlignment(Qt.AlignCenter)
        self.sub_tokenLine.setAlignment(Qt.AlignCenter)

        #Add to layout
        layout.addWidget(self.title)
        #layout.addWidget(self.lineBreak1)
        layout.addWidget(self.car0)
        layout.addWidget(self.car1)
        layout.addWidget(self.car2)
        layout.addWidget(self.car3)
        layout.addWidget(self.car4)
        layout.addWidget(self.car5)
        layout.addWidget(self.car6)
        layout.addWidget(self.tokenLine)
        layout.addWidget(self.sub_tokenLine)
        pybutton = QPushButton('Take a Step', self)
        pybutton.resize(50,50)
       	layout.addWidget(pybutton) #pybutton.move(50, 50)        
        pybutton.clicked.connect(self.step_message)

   

        self.setLayout(layout) 
        self.setMinimumSize(600, 800)
        self.setWindowTitle("Leader Model Checker")
        # we need the signal so the event is processed on the GUI thread
        # source: https://github.com/Sensirion/libsensors-python/blob/master/streaming_plot_client.py
        self._mqtt_client.on_message = lambda client, userdata, msg: self.client_handler.emit(msg)
        self.client_handler.connect(self.on_client_message)

    # Handlers for each message
    

    def on_client_message(self, msg):
        print("Received" + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
        myString = str(msg.payload.decode('utf-8')).split("$$$$")
        #DIRECT_CAR+"$$$$"+carID+"$$$$"+qzqueueID+"$$$$"+current+"$$$$command$$$$"+next;
        # car id 0-4
        # qz 0-4
        #Messages expecting
        #$$$$DIRECT_CAR$$$$1$$$$qz0$$$$EXIT$$$$goForward$$$$qz0
        #$$$$DIRECT_CAR$$$$1$$$$qz0$$$$OUT$$$$goForward$$$$qz0
        if len(myString)==7 or len(myString)==3 :
            print("_---------->" + (myString[1]))
            pass
            
        else:
            print("length of string:" + str(len(myString)))
            return
        if (myString[1] == "DIRECT_CAR") or (myString[1] == "TOKEN") or (myString[1] == "SUBTOKEN") :
            self.messageQueue.append(myString)


    def step_message(self):
        if len(self.messageQueue) == 0:
            return  
        myString= self.messageQueue.pop(0)
      
        if len(myString)==7:
            #print("length of steam:" + str(len(myString)))
             #return
        
            if (myString[1] == "DIRECT_CAR" and myString[2] == "0") :
                self.update_label_something0(myString[2], myString[3],myString[4],myString[5],myString[6])
            
            elif  (myString[1] == "DIRECT_CAR" and myString[2] == "1"):
                self.update_label_something1(myString[2], myString[3],myString[4],myString[5],myString[6])
        

            elif  (myString[1] == "DIRECT_CAR" and myString[2] == "2"):
                self.update_label_something2(myString[2], myString[3],myString[4],myString[5],myString[6])

        
            elif ( myString[1] == "DIRECT_CAR" and myString[2] == "3"):
                self.update_label_something3(myString[2], myString[3],myString[4],myString[5],myString[6])

            elif ( myString[1] == "DIRECT_CAR" and myString[2] == "4"):
                self.update_label_something4(myString[2], myString[3],myString[4],myString[5],myString[6])

            elif ( myString[1] == "DIRECT_CAR" and myString[2] == "5"):
                self.update_label_something5(myString[2], myString[3],myString[4],myString[5],myString[6])

            elif ( myString[1] == "DIRECT_CAR" and myString[2] == "6"):
                self.update_label_something6(myString[2], myString[3],myString[4],myString[5],myString[6])
       
 

        elif len(myString)==3: 

            if ( myString[1] == "SUBTOKEN"):
                self.update_label_something_subtoken(myString[2])


            elif ( myString[1] == "TOKEN"):
                self.update_label_something_token(myString[2])
    #TODO Figure out when the car moves form QZ ->l1 ->l2 ->EXIT to show that its light moves.

    def update_fluent(self, current,nextID):
        print( "Message parsing " + str(current) +" " + str(nextID) )
        if nextID == "l0":
            self.countCZ0 = self.countCZ0 +1
 
        elif nextID == "l1":
            self.countCZ1 = self.countCZ1 +1

        elif nextID == "l2":
            self.countCZ2 = self.countCZ2 +1

        elif nextID == "l3":
            self.countCZ3 = self.countCZ3 +1

        if current == "l0":
            self.countCZ0 = self.countCZ0 -1  
 
        elif current == "l1":
            self.countCZ1 = self.countCZ1 -1  
        
        elif current == "l2":
            self.countCZ2 = self.countCZ2 -1  

        elif current == "l3":
            self.countCZ3 = self.countCZ3 -1  

        print(str( self.countCZ0)+"||||"+str( self.countCZ1)+"||||" +str( self.countCZ2)+"||||"+str( self.countCZ3))

        action="FLUENT||||count||||"+str( self.countCZ0)+"||||"+str( self.countCZ1)+"||||" +str( self.countCZ2)+"||||"+str( self.countCZ3)
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '||||'+action
        self._mqtt_client.publish(self._mqtt_topic, mqtt_message) 
        #timestamp||||FLUENT||||CZ||||CZ0Count||||CZ1count||||CZ2Count||||CZ3Count
 
    def update_label_something0(self, carID,qzqueueID,current,command,nextID):
        temp0 = ("Lane " + qzqueueID + "  car " + carID+ " to go from   "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car0.setText(temp0)
        self.update_fluent(current,nextID) 
 
    def update_label_something1(self, carID,qzqueueID,current,command,nextID):
        temp1 = ("Lane " + qzqueueID + "  car " + carID+ " to go from  "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car1.setText(temp1)
        self.update_fluent(current,nextID)

    def update_label_something2(self, carID,qzqueueID,current,command,nextID):
        temp2 = ("Lane " + qzqueueID + "  car " + carID+ " to go from  "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car2.setText(temp2)
        self.update_fluent(current,nextID)

    def update_label_something3(self, carID,qzqueueID,current,command,nextID):
        temp3 = ("Lane " + qzqueueID + "  car " + carID+ "  to go from  "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car3.setText(temp3)
        self.update_fluent(current,nextID)

    def update_label_something4(self, carID,qzqueueID,current,command,nextID):
        temp4 = ("Lane " + qzqueueID + "  car " + carID+ " to go from  "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car4.setText(temp4)
        self.update_fluent(current,nextID)

    def update_label_something5(self, carID,qzqueueID,current,command,nextID):
        temp5 = ("Lane " + qzqueueID + "  car " + carID+ " to go from "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car5.setText(temp5)
        self.update_fluent(current,nextID)
    def update_label_something6(self, carID,qzqueueID,current,command,nextID):
        temp6 = ("Lane " + qzqueueID + "  car " + carID+ " to go from "  + current+     "  via         " + command +    "   to      " +nextID )
        self.car6.setText(temp6)
        self.update_fluent(current,nextID)

    def update_label_something_subtoken(self, laneID):
        temp6 = (laneID)
        self.sub_tokenLine.setText(temp6)
        action="FLUENT||||SUBTOKEN||||"+str(laneID)
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '||||'+action
        self._mqtt_client.publish(self._mqtt_topic, mqtt_message) 
    #timestamp||||FLUENT||||SUBTOKEN||||IDWHOHASTOKEN
    def update_label_something_token(self, laneID):
        temp6 = (laneID)
        self.tokenLine.setText(temp6)

        action="FLUENT||||TOKEN||||"+str(laneID)
        timestamp = dt.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
        mqtt_message = "[%s] %s " % (timestamp,ip_addr) + '||||'+action
        self._mqtt_client.publish(self._mqtt_topic, mqtt_message) 


def main():
    # Instantiate the MQTT client
    mqtt_client = paho.Client()
    mqtt_topic = topicname + '/' + socket.gethostname()
    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, 1883, keepalive=600) # UI is only a listener
    mqtt_client.subscribe(topicname + "/#")
    app = QApplication(sys.argv)
    mainWindow = mainClass(mqtt_client,mqtt_topic)
    mainWindow.show()
    mqtt_client.loop_start()
    # Start the GUI
    try:
        sys.exit(app.exec_())
    finally:
        mqtt_client.loop_stop()	
if __name__ == '__main__':
    main()
