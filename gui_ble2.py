import os
import subprocess
from guizero import App, Text, PushButton

def resetfiles():
    subprocess.run(["python", "clearfiles.py"])
def startBLE():
    subprocess.run(["python", "testLoop.py"])

app = App(bg="lightblue", width="170", height="200")
text0 = Text(app, text="Bluetooth Manager", align="top", width="fill")
text1 = Text(app, align="top", width="fill")
button0 = PushButton(app, text="Click to Connect", command=startBLE, 
					align="top")
button1= PushButton(app, text="Reset", command=resetfiles, 
					align="top")

app.display()
