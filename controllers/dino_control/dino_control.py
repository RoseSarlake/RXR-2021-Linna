"""dino_control controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Keyboard
TIME_STEP = 64
max_speed = 6.28
# create the Robot instance.
robot = Robot()
keyboard = Keyboard()
keyboard.enable(TIME_STEP)
# get the time step of the current world.

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
right_motor = robot.getDevice('motor1')
left_motor = robot.getDevice('motor2')
front_motor = robot.getDevice('motor3')

right_motor.setPosition(float('inf'))
right_motor.setVelocity(0.0)
left_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
front_motor.setPosition(float('inf'))
front_motor.setVelocity(0.0)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(TIME_STEP) != -1:

    key=keyboard.getKey()

    left_speed = 0.3* max_speed
    right_speed = 0.3 * max_speed
    front_speed = 0.3 * max_speed
    
    if (key==ord('W')):
        print ('W is pressed')
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
        front_motor.setVelocity(front_speed)
    if (key==ord('S')):
        print ('S is pressed')
        left_motor.setVelocity(-left_speed)
        right_motor.setVelocity(-right_speed)
        front_motor.setVelocity(-front_speed) 
    if (key==ord('A')):
        print ('A is pressed')
        left_motor.setVelocity(-left_speed*2)
        right_motor.setVelocity(right_speed*2) 
    if (key==ord('D')):
        print ('D is pressed')
        left_motor.setVelocity(left_speed*2)
        right_motor.setVelocity(-right_speed*2)
    if (key==ord('X')):
        print ('X is pressed')
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
