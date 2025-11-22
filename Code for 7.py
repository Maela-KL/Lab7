from machine import Pin, PWM
import time
from servo_translator import translate
# Defining each part of the board
shoulder = PWM(Pin(15))
elbow = PWM(Pin(1))
wrist = PWM(Pin(2))
# Now the frequency of each servo motor 
shoulder.freq(50)
elbow.freq(50)
wrist.freq(50)
# IG we need # to redefine translate here too
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
# We need safe wrist movements for up and down
def wrist_up():
    wrist.duty_u16(translate(0))
    time.sleep(0.5)
def wrist_down():
    wrist.duty_u16(translate(90))
    time.sleep(0.5)
# We have to read a g-code file
def read_gcode(path):
    with open(path) as file:
        lines = file.readlines()
        print(lines)
        for line in file:
            lines.append(line.strip())
    return lines
# Now we need to parse the g-code commands
#{"cmd": "G1", "s": 90, "e": 45}
def parse_gcode(lines):
    for line in lines:
        if line.startswith('s'):
            angle = int(line['s'])
            shoulder.duty_u16(translate(angle))
            time.sleep(0.5)
        elif line.startswith('e'):
            angle = int(line['e'])
            elbow.duty_u16(translate(angle))
            time.sleep(0.5)
        elif line.startswith('w'):
            wrist_up()
            time.sleep(0.5)
        elif line.startswith('u'):
            wrist_down()
            time.sleep(0.5)
        return line
# execute the g-code commands
def execute_gcode(lines):
    line = lines["lines"]
    if line == 'G1':
        parse_gcode(lines)
# Main function to run the program
def main():
    lines = read_gcode('circle.gcode')
    execute_gcode(lines)
    print("Beginning plotter...")
    for line in lines:
        execute_gcode(line)