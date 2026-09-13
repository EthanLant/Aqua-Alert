import os
from guizero import App, Text, PushButton

def callconnect():
    os.system("python connect.py")
    text1 = Text(app, text="Connecting...", grid=[0,2])
    #f=open("receive.txt")
    #terminal = f.read()
    #text2 = Text(app, text=terminal, grid=[0,3])

app = App(layout="grid")
text0 = Text(app, text="AquaAlert Control Center", grid=[0,0])
button0 = PushButton(app, text="Pair the Device", command=callconnect, 
					grid=[0,1])
app.display()
