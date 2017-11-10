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
    wul = "????"
    wur = "????"
    wul1 = "????"
    wur1 = "????"
    wul2 = "????"
    wur2 = "????"
    
    # Start out true, only can turn to False once
    weak_until = True
    weak_until1 = True
    weak_until2 = True
   
    def __init__(self, mqtt_client):
        super().__init__()
        self._mqtt_client = mqtt_client
        self.initUI()

    def initUI(self): 
        #This is the layout
        layout = QVBoxLayout(self)
        #Add the two layouts for the scroll boxes

        layout.setContentsMargins(10, 0, 10, 600)
        layout.setSpacing(0)
        #layout.insertStretch(0,0);
        #Intro message
        self.introductionText = QLabel(" Welcome to our program\n\n")
        self.introductionText.setAlignment(Qt.AlignCenter) 
        #Add text to layout
        layout.addWidget(self.introductionText)

        #Line spce
        lineSpace =  QLabel()
        #Add different labels 
        title = QLabel()
        self.weakUntilAssert= QLabel()
        self.weakTimeStamp = QLabel()
        self.weakStatus = QLabel()
    
        title1 = QLabel()
        self.weakUntilAssert1= QLabel()
        self.weakTimeStamp1 = QLabel()
        self.weakStatus1 = QLabel()
        

        title2 = QLabel()
        self.weakUntilAssert2= QLabel()
        self.weakTimeStamp2 = QLabel()
        self.weakStatus2 = QLabel()

        lineBreak=QLabel()   
        lineBreak1=QLabel()   
     
        title.setText("Fluent0")
        self.weakUntilAssert.setText("Fluent goes here")
        self.weakTimeStamp.setText("Time Stamp: Not updated yet")
        self.weakStatus.setText("Status: OK")
  
        lineBreak.setText("---------------------------------------------------------------------------")       
        lineBreak1.setText("---------------------------------------------------------------------------")       
        title1.setText("Fluent1")
        self.weakUntilAssert1.setText("Fluent goes here")
        self.weakTimeStamp1.setText("Time Stamp: Not updated yet")
        self.weakStatus1.setText("Status: ok")

        title2.setText("Fluent2")
        self.weakUntilAssert2.setText("Fluent goes here")
        self.weakTimeStamp2.setText("Time Stamp: Not updated yet")
        self.weakStatus2.setText("Status: ok")

	
        title.setAlignment(Qt.AlignCenter)
        self.weakUntilAssert.setAlignment(Qt.AlignLeft)
        self.weakTimeStamp.setAlignment(Qt.AlignLeft)
        self.weakStatus.setAlignment(Qt.AlignLeft)
       
        title1.setAlignment(Qt.AlignCenter)
        self.weakUntilAssert1.setAlignment(Qt.AlignLeft)
        self.weakTimeStamp1.setAlignment(Qt.AlignLeft)
 
        title2.setAlignment(Qt.AlignCenter)
        self.weakUntilAssert2.setAlignment(Qt.AlignLeft)
        self.weakTimeStamp2.setAlignment(Qt.AlignLeft)
        


        #Add to layout
        layout.addWidget(title)
        layout.addWidget(self.weakUntilAssert)
        layout.addWidget(self.weakTimeStamp)
        layout.addWidget(self.weakStatus)

        layout.addWidget(lineBreak)
           
        layout.addWidget(title1)
        layout.addWidget(self.weakUntilAssert1)
        layout.addWidget(self.weakTimeStamp1)
        layout.addWidget(self.weakStatus1)
        #Add layout and widgets to window , set window size, name window
        
        layout.addWidget(lineBreak1)
 
        layout.addWidget(title2)
        layout.addWidget(self.weakUntilAssert2)
        layout.addWidget(self.weakTimeStamp2)
        layout.addWidget(self.weakStatus2)
        

        self.setLayout(layout) 
        self.setMinimumSize(600, 800)
        self.setWindowTitle("Leader Model Checker")
        # we need the signal so the event is processed on the GUI thread
        # source: https://github.com/Sensirion/libsensors-python/blob/master/streaming_plot_client.py
        self._mqtt_client.on_message = lambda client, userdata, msg: self.client_handler.emit(msg)
        self.client_handler.connect(self.on_client_message)

    # Handlers for each message
    #Weak0
    def update_label_weak_until_left(self, l, ts):
        print("update_label_weak_until_left called")
        self.wul = l
        self.weakUntilAssert.setText("!({} W {})".format(self.wul, self.wur))
        self.weakTimeStamp.setText("Timestamp: {}".format(ts))
    def update_label_weak_until_right(self, r, ts):
        print("update_label_weak_until_right called")
        self.wur = r
        self.weakUntilAssert.setText("!({} W {})".format(self.wul, self.wur))
        self.weakTimeStamp.setText("Timestamp: {}".format(ts))
    
    def update_label_weak_until_status(self, status, ts):
        print("update_label_weak_until_status called")
        if self.weak_until == False:
            return
        elif status == "Failed":
            self.weak_until = False
        self.weakStatus.setText("Status: {}".format(status))
        self.weakTimeStamp.setText("Timestamp: {}".format(ts))
    
    #Weak1
    def update_label_weak_until_left1(self, l, ts):
        print("update_label_weak_until_left called")
        self.wul1 = l
        self.weakUntilAssert1.setText("!({} W {})".format(self.wul1, self.wur1))
        self.weakTimeStamp1.setText("Timestamp: {}".format(ts))
    def update_label_weak_until_right1(self, r, ts):
        print("update_label_weak_until_right called")
        self.wur1 = r
        self.weakUntilAssert1.setText("!({} W {})".format(self.wul1, self.wur1))
        self.weakTimeStamp1.setText("Timestamp: {}".format(ts))
    
    def update_label_weak_until_status1(self, status, ts):
        print("update_label_weak_until_status called")
        if self.weak_until1 == False:
            return
        elif status == "Failed":
            self.weak_until1 = False
        self.weakStatus1.setText("Status: {}".format(status))
        self.weakTimeStamp1.setText("Timestamp: {}".format(ts))
   
    #Weak2 
    def update_label_weak_until_left2(self, l, ts):
        print("update_label_weak_until_left called")
        self.wul2 = l
        self.weakUntilAssert2.setText("!({} W {})".format(self.wul2, self.wur2))
        self.weakTimeStamp2.setText("Timestamp: {}".format(ts))
    def update_label_weak_until_right2(self, r, ts):
        print("update_label_weak_until_right called")
        self.wur2 = r
        self.weakUntilAssert2.setText("!({} W {})".format(self.wul2, self.wur2))
        self.weakTimeStamp2.setText("Timestamp: {}".format(ts))
    
    def update_label_weak_until_status2(self, status, ts):
        print("update_label_weak_until_status called")
        if self.weak_until2 == False:
            return
        elif status == "Failed":
            self.weak_until2 = False
        self.weakStatus2.setText("Status: {}".format(status))
        self.weakTimeStamp2.setText("Timestamp: {}".format(ts))
    


    def on_client_message(self, msg):
        print("Received" + ", ".join([msg.topic, msg.payload.decode('utf-8') + "\n"]))
        myString = str(msg.payload.decode('utf-8')).split("$$$$")
        #Check WeakUntill
        #Check 1
        if len(myString) == 4 and myString[1] == "lw" and myString[2] == "0" :
            self.update_label_weak_until_left(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "rw" and myString[2] == "0":
            self.update_label_weak_until_right(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "W" and myString[2] == "0" and myString[3] == "Cheater":
            self.update_label_weak_until_status(myString[3], myString[0])
        #Check 2
        if len(myString) == 4 and myString[1] == "lw" and myString[2] == "1" :
            self.update_label_weak_until_left1(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "rw"and myString[2] == "1":
            self.update_label_weak_until_right1(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "W"and myString[2] == "1" and myString[3] == "Cheater":
            self.update_label_weak_until_status1(myString[3], myString[0])
        #Check 3
        if len(myString) == 4 and myString[1] == "lw" and myString[2] == "2" :
            self.update_label_weak_until_left2(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "rw"and myString[2] == "2":
            self.update_label_weak_until_right2(myString[3], myString[0])
        elif len(myString) == 4 and myString[1] == "W"and myString[2] == "2" and myString[3] == "Cheater":
            self.update_label_weak_until_status2(myString[3], myString[0])

def main():
    # Instantiate the MQTT client
    mqtt_client = paho.Client()
    mqtt_topic = topicname + '/' + socket.gethostname()
    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.connect(broker, 1883, keepalive=600) # UI is only a listener
    mqtt_client.subscribe(topicname + "/#")
    app = QApplication(sys.argv)
    mainWindow = mainClass(mqtt_client)
    mainWindow.show()
    mqtt_client.loop_start()
    # Start the GUI
    try:
        sys.exit(app.exec_())
    finally:
        mqtt_client.loop_stop()	
if __name__ == '__main__':
    main()
