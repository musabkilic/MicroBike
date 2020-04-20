import microbit
import time
from pynput.keyboard import Key, Controller

#Function for Changing a Key
def changeKeyState(key, value):
	global keyboard_keys

	#Change Only Neccessary
	if value!=keyboard_keys.get(key, False):
		if value:
			keyboard.press(key)
		else:
			keyboard.release(key)

	keyboard_keys[key] = value

#Specify Keyboard
keyboard = Controller()
#Set Accelerometer Values
previous_values = microbit.accelerometer.get_values()
keyboard_keys = {}
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
	changeKeyState(Key.up, y>400)
	changeKeyState(Key.right, x>60)
	changeKeyState(Key.left, x<-60)
	changeKeyState(Key.shift, motion>500)

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
