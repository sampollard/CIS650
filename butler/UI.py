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
MY_NAME = 'UI_weak_until'
broker = 'iot.eclipse.org'
topicname = "cis650prs"

# Get your IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_addr = str(s.getsockname()[0])
print('IP address: {}'.format(ip_addr))
s.close()


class mainClass(QWidget):
    #client_message = QtCore.pyqtSignal(object)
    #client_message = pyqtSignal(object)
    #client_message = pyqtSignal([str])
    #trigger = pyqtSignal()

   
    #def test(self):
    #    print("hello test")

    

    def __init__(self, mqtt_client, parent = None):
        super().__init__()
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
        lineSpace =  QLabel()
        #Add different labels 
        title1 = QLabel()
        weakUntillAssert= QLabel()
        weakTimeStamp = QLabel()
        weakStatus = QLabel()
    
        lineBreak=QLabel()   
     
        title2 = QLabel()
        progressProperty= QLabel()
        progressPropertyTimeStamp = QLabel()
        progressPropertyStatus = QLabel()
        
        title1.setText("Weak untill Assert")
        weakUntillAssert.setText("! lw W rw ")
        weakTimeStamp.setText("Time Stamp: No updated yet")
        weakStatus.setText("Status: ok/failed")
  
        lineBreak.setText("---------------------------------------------------------------------------")       
 
        title2.setText("Progress property")
        progressProperty.setText("lp -->  rp ")
        progressPropertyTimeStamp.setText("Time Stamp: No updated yet")
        progressPropertyStatus.setText("Status: ok/failed")
	
        title1.setAlignment(Qt.AlignCenter)
        weakUntillAssert.setAlignment(Qt.AlignLeft)
        weakTimeStamp.setAlignment(Qt.AlignLeft)
        weakStatus.setAlignment(Qt.AlignLeft)
       
        lineBreak.setAlignment(Qt.AlignCenter)
 
        title2.setAlignment(Qt.AlignCenter)
        progressProperty.setAlignment(Qt.AlignLeft)
        progressPropertyTimeStamp.setAlignment(Qt.AlignLeft)
        progressPropertyStatus.setAlignment(Qt.AlignLeft)

        layout.addWidget(title1)
        layout.addWidget(weakUntillAssert)
        layout.addWidget(weakTimeStamp)
        layout.addWidget(weakStatus)

        layout.addWidget(lineBreak)
           
        layout.addWidget(title2)
        layout.addWidget(progressProperty)
        layout.addWidget(progressPropertyTimeStamp)
        layout.addWidget(progressPropertyStatus)
        #Add layout and widgets to window , set window size, name window
        self.setLayout(layout)
        
        self.setMinimumSize(600, 800)
        self.setWindowTitle("Model Checker")
     
    
    def update_label1():
        sweakUntillAssert.setText("! adfasdlasdfasdw W rw ")
        weakTimeStamp.setText("Time safdasStamp: No updatasdfed yet")
        weakStatus.setText("Status:asdf ok/fasdfailed")
 
    def update_label2():
        self.progressProperty.setText("lp --adsfasdf>  rp ")
        self.progressPropertyTimeStamp.setText("Timeadsfasd Stamp: No updated yet")
        self.progressPropertyStatus.setText("Status: ok/fasdfasdiled")


 
    def handle_trigger(self):
        print("Trigger signal received")

    def on_client_message(self, _userdata, msg):
        print("on client msg called")
        print(msg.payload)
        mainClass.update_label1()   
        '''
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
        print("Leaving client msg")
        '''
        return
 
   
    def on_connect(elf, _userdata, flags_dict, result):
        print("Connected")

    def on_disconnect(self,client, userdata, rc):
        print("Disconnected in a normal way")
        #graceful so won't send will

    def on_log(self, _userdata, level, buf):
        pass

    
    mqtt_client2 = paho.Client()

    # set up handlers
    mqtt_client2.on_connect = on_connect
    mqtt_client2.on_message = on_client_message
    mqtt_client2.on_disconnect = on_disconnect
    mqtt_client2.on_log = on_log
    
    mqtt_topic2 =  '/' + socket.gethostname()

    mqtt_client2.will_set(mqtt_topic2, '______________Will of '+ 'testing '+' _________________\n\n', 0, False)
    broker = 'iot.eclipse.org'
    mqtt_client2.connect(broker, 1883)
    mqtt_client2.subscribe("cis650prs/#") #subscribe to all students in class
    mqtt_client2.loop_start()
     

def main():
            # Instantiate the MQTT client
    mqtt_client = paho.Client()
    mqtt_topic = topicname + '/' + socket.gethostname()   
    mqtt_client.will_set(mqtt_topic, '______________Will of '+MY_NAME+' _________________\n\n', 0, False)
    mqtt_client.subscribe("#")
    #mqtt_client.subscribe(topicname + "/#")
    app = QApplication(sys.argv)
    mainWindow = mainClass(app)#,mqtt_client)
    mainWindow.show()
    
    #mqtt_client.connect(broker, 1883)
    #mqtt_client.loop_start() 
    try:
        sys.exit(app.exec_())
    finally:
        mqtt_client.loop_stop()

	
if __name__ == '__main__':
    main()
