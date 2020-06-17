from __future__ import unicode_literals
import sys
from PyQt5 import QtWidgets, QtGui
import Testaplic
import testard
import csv
import os
import paho.mqtt.client as mqttClient
import time


stop_flag = False
count = 0
Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("/user/Igorabcdefg/test2")
        client.subscribe("/user/Igorabcdefg/start")
        global Connected  # Use global variable
        Connected = True  # Signal connection
        global count
        count += 1


    else:
        print("Connection failed")


Dist = []
Time = []
is_arduino_started = False
client = None


def start():
    global is_arduino_started
    if is_arduino_started == False:
        client.publish("/user/Igorabcdefg/test123", "z")
    if is_arduino_started == True:
        client.publish("/user/Igorabcdefg/test123", "a")
        print("Sended a")


def on_message(client, userdata, message):
    command = str(message.payload).replace('b', "")
    command = command.replace("'", "")
    print(command)

    if str(command) == '1':
        global is_arduino_started
        is_arduino_started = True
        start()
        print("arduino_started")

    if str(command) == "start":
        print("Starting experiment")
    if str(command) == "finish":
        print("End of experiment")
        print(Dist)
        print(Time)
        with open("SensorDataStore.csv", "w", newline="") as file:
            print("here1")
            writer = csv.writer(file)
            print("here2")
            length = 0
            if len(Time) > len(Dist):
                length = len(Dist)
            else:
                length = len(Time)
            for i in range(length):
                writer.writerow([Time[i], Dist[i]])
            print("here3")
        global stop_flag
        stop_flag = True
        global Connected
        Connected = False
        print("changed connected")
        client.loop_stop()
        print("loop_stop")




    if str(command) != "start": #& str(command) != "finish" & str(command) != "1":
        if command[0] == "d":
            distance = float(command.replace('d', ""))
            Dist.append(distance)
        if command[0] == "t":
            Time.append(float(command.replace('t', "")))

def connect_to_mqtt():
    Dist.clear()
    Time.clear()
    broker_address = "mqtt.by"  # Broker address
    port = 1883  # Broker port
    user = "Igorabcdefg"  # Connection username
    password = "txok6gzz"  # Connection password
    global client

    client = mqttClient.Client()  # create new instance
    client.username_pw_set(user, password=password)  # set username and password
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message  # attach function to callback

    client.connect(broker_address, port=port)  # connect to broker

    client.loop_start()  # start the loop
    print("start")
    global Connected
    while Connected == False:
        time.sleep(0.1)
        print("while1")
    start()
    print("start end")

    while Connected == True:
        time.sleep(0.1)

    if Connected == False:
        global count
        global stop_flag
        while count == 0:
            time.sleep(0.1)
        if count > 0:
            client.disconnect()
            client.loop_stop()
            return


    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("exiting")

        client.disconnect()
        client.loop_stop()


class ExampleApp(QtWidgets.QMainWindow, Testaplic.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Start)

    def Start(self):
        connect_to_mqtt()
        if os.stat("SensorDataStore.csv").st_size != 0:
            testard.generate_all()
            path = os.getcwd()
            self.label_2.setPixmap(QtGui.QPixmap(path+"/img/graph.png"))
            self.label_3.setPixmap(
                QtGui.QPixmap(path+"/img/graph1.png"))
            self.label_4.setPixmap(
                QtGui.QPixmap(path+"/img/graph2.png"))
            print("updated")
        else:
            print("no data, return cart to its initial position")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()


