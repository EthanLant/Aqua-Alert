import subprocess
from guizero import App, Text, PushButton

def monitor():
	alertmessage.repeat(200, monitor)
	with open("alarm.txt") as f2:
		alert = f2.read()
		if (alert == "alert"):
			alertmessage.value = "WATER DETECTED"
			alertmessage.cancel(monitor)
			

def check():
	with open("receive.txt") as f1:
		message = f1.read()
		if message == "Connected":
			buttonstart = PushButton(app, text="Start Monitoring", command=monitor,
						width="fill")
			textmessage.value = "Connected"	

app = App(bg="green", width="400")
text0 = Text(app, text="AquaAlert", width="fill", align="top")
button0 = PushButton(app, text="Check Connection",
					command=check, width="fill", align="top")
textdisplay = Text(app, text="Connection:", width="fill", 
					align="top")
textmessage = Text(app, width="fill", align="top")
alertmessage = Text(app, color="red", width="fill", align="top")
app.display()
