from time import sleep

def main():
	#with open("receive.txt", "w") as f:
		
		#f.write("Connected")
		
	sleep(20)
	
	with open("alarm.txt", "a") as f:
		f.truncate(0)
		f.write("alert")
    
main()
