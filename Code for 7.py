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
    wrist.duty_u16(translate(30))
    time.sleep(0.5)
#Movement of shoulder and elbow
def move_shoulder(angle):
    shoulder.duty_u16(translate(angle))
    time.sleep(0.5)
def move_elbow(angle):
    elbow.duty_u16(translate(angle))
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
#{"cmd": "G1", "s": 90, "e": 45}¸
def parse_gcode_line(line):
    parts = line.split()
    cmd = parts[0]

    parsed = {"cmd": cmd}

    for p in parts[1:]:
        if p.startswith("S"):
            parsed["S"] = int(p[1:])
        elif p.startswith("E"):
            parsed["E"] = int(p[1:])

    return parsed
# execute the g-code commands
def execute_command(cmd):
    command= cmd["cmd"]
    if command == 'G1':
        if 'S' in cmd:
            move_shoulder(cmd["S"])
        if 'E' in cmd:
            move_elbow(cmd["E"])
    elif command == 'M3':
        wrist_up()
    elif command == 'M5':
        wrist_down()
# Main function to run the program
def main():
    lines = read_gcode('circle.gcode')
    execute_command(lines)
    print("Beginning plotter...")
    for line in lines:
        execute_command(line)
        print("Finished executing line.")
