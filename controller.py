import microbit
import time
from pykeyboard import PyKeyboard

#Function for Changing a Key 
def changeKeyState(key, value, key_name):
	global keyboard_keys

	#Change Only Neccessary
	if value!=keyboard_keys[key_name]:
		if value:
			keyboard.press_key(key)
		else:
			keyboard.release_key(key)

	keyboard_keys[key_name] = value

#Specify Keyboard
keyboard = PyKeyboard()
#Set Accelerometer Values
previous_values = microbit.accelerometer.get_values()
#Set Keyboard Keys
keyboard_keys = {"L":False,"R":False,"F":False,"S":False}
#Set Images
stable = microbit.Image("00000:00000:99999:00000:00000")
images = {"N": microbit.Image.ARROW_N,
		  "NE": microbit.Image.ARROW_NE,
		  "NW": microbit.Image.ARROW_NW,
		  "E": microbit.Image.ARROW_E,
		  "W": microbit.Image.ARROW_W,
		  "": stable}

#Wait for User to Press a Button
while 1:
	#Blink
	microbit.display.show(microbit.Image.ARROW_W)
	time.sleep(0.5)
	microbit.display.clear()

	#Start the Program if a Button is Pressed
	if microbit.button_a.was_pressed() or microbit.button_b.was_pressed():
		break
	time.sleep(0.5)

#Start the Loop
while 1:
	#Get Accelerometer Values
	accelerometer_values = microbit.accelerometer.get_values()
	x,y,z = accelerometer_values

	#Calculate Avarege Motion in X,Y,Z Directions
	motion = sum(map(lambda x:abs(accelerometer_values[x]-previous_values[x]),range(3)))/3

	#Change Direction
	changeKeyState(keyboard.up_key,y>400,"F")
	changeKeyState(keyboard.right_key,x>60,"R")
	changeKeyState(keyboard.left_key,x<-60,"L")
	changeKeyState(keyboard.shift_key,motion>500,"S")

	#Set Direction to Show
	direction = ""
	if y>400:
		direction += "N"
	if x>60:
		direction += "E"
	elif x<-60:
		direction += "W"

	#Show the Direction
	microbit.display.show(images[direction])
	#Set Current Accelerometer Values to Previous
	previous_values = accelerometer_values