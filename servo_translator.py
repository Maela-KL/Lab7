# Submit this file via brightspace
from machine import Pin, PWM
import time
servo = PWM(Pin(0))
servo.freq(50)
# You should not modify the signature (name, input, return type) of this function
def translate(angle: float) -> int: 
	"""
	Converts an angle in degrees to the corresponding input
	for the duty_u16 method of the servo class
	See https://docs.micropython.org/en/latest/library/machine.PWM.html for more
	details on the duty_u16 method
	"""
	# Map angle (0-180) to pulse width (500-2500 microseconds)
	servo_min = 1638
	servo_max = 8192
	# Calculate duty cycle
	duty = int(65535 * ((500 + (2000 * angle / 180)) / 20000))
	return duty
print(translate(90))
# Move to 90 degrees
servo.duty_u16(translate(90))
time.sleep(1)
# Move to 0 degrees
servo.duty_u16(translate(0))