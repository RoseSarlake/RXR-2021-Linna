from controller import Robot,DistanceSensor,Motor,Camera,Keyboard,GPS,InertialUnit
TIME_STEP = 16
MAX_SPEED = 6.28

robot = Robot()

camera = Camera("my_cam")
camera.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)

keyboard = Keyboard()
keyboard.enable(TIME_STEP)

gps = GPS("gp")
gps.enable(TIME_STEP)

imu = InertialUnit("imu")
imu.enable(TIME_STEP)

rm = robot.getDevice("rm")
rotate = 0

# distance sensors
ds = []
dsNames = ['ds_right', 'ds_left']
for i in range(2):
    ds.append(robot.getDevice(dsNames[i]))
    ds[i].enable(TIME_STEP)
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('-inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0

# start the loop
while robot.step(TIME_STEP) != -1:
    # wheels
    leftSpeed = MAX_SPEED/2
    rightSpeed = MAX_SPEED/2
    # leftSpeed = 0
    # rightSpeed = 0
    if avoidObstacleCounter > 0:
        avoidObstacleCounter -= 1
        leftSpeed = 0 #MAX_SPEED/2
        rightSpeed = -MAX_SPEED/2
    else:  # read sensors
        for i in range(2):
            if ds[i].getValue() < 800.0:
                avoidObstacleCounter = 100
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
    
    #GPS
    x = gps.getValues()[0]
    y = gps.getValues()[1]
    z = gps.getValues()[2]
    print("##########################")
    print("current location: x="+ str(x)+",y="+str(y)+",z="+ str(z))
    
    #IMU
    Angle_x = imu.getRollPitchYaw()[0]
    Angle_y = imu.getRollPitchYaw()[1]
    Angle_z = imu.getRollPitchYaw()[2]

    # camera
    num_objects = camera.getRecognitionNumberOfObjects()
    objects = camera.getRecognitionObjects()
    for object in objects:
        id_object = object.get_id()
        target = object.get_model()
        size = object.get_size_on_image()
        #print(sum(size))
        [dino_x,dino_y,dino_z] = object.get_position()
        if target == b'dinosaur':
            print("find dino")
            print ('id ' + str(id_object), 'position: (x)'+ str(dino_x))
            # stop if close enough
            if sum(size)>=850:
               wheels[0].setVelocity(0)
               wheels[1].setVelocity(0)
               wheels[2].setVelocity(0)
               wheels[3].setVelocity(0)
           # approach if not close
           # when the target at back 
            else:
                if 0.785<=rotate%6.28<2.355:
                   # back left
                    if dino_x>0: 
                        wheels[0].setVelocity(-leftSpeed/3)
                        wheels[1].setVelocity(-rightSpeed)
                        wheels[2].setVelocity(-leftSpeed/3)
                        wheels[3].setVelocity(-rightSpeed)
                   # back right
                    if dino_x<0:
                        wheels[0].setVelocity(-leftSpeed)
                        wheels[1].setVelocity(-rightSpeed/3)
                        wheels[2].setVelocity(-leftSpeed)
                        wheels[3].setVelocity(-rightSpeed/3)
               # when the target in the right
                if 2.355<=rotate%6.28<3.925:
                   # back right
                    if dino_x>0:
                        wheels[0].setVelocity(-leftSpeed)
                        wheels[1].setVelocity(rightSpeed/3)
                        wheels[2].setVelocity(-leftSpeed)
                        wheels[3].setVelocity(rightSpeed/3)
                   # front right
                    if dino_x<0:
                        wheels[0].setVelocity(leftSpeed)
                        wheels[1].setVelocity(-rightSpeed/3)
                        wheels[2].setVelocity(leftSpeed)
                        wheels[3].setVelocity(-rightSpeed/3)
               # when the target in front of suitcase
                if 3.925<=rotate%6.28<5.495:
                    # just in front
                    if 4.5<=rotate%6.28<4.9 and -0.1<dino_x<0.1:
                        wheels[0].setVelocity(leftSpeed)
                        wheels[1].setVelocity(rightSpeed)
                        wheels[2].setVelocity(leftSpeed)
                        wheels[3].setVelocity(rightSpeed)
                   # front right
                    elif dino_x>0:
                        wheels[0].setVelocity(leftSpeed)
                        wheels[1].setVelocity(rightSpeed/3)
                        wheels[2].setVelocity(leftSpeed)
                        wheels[3].setVelocity(rightSpeed/3)
                   # front left     
                    elif dino_x<0:
                        wheels[0].setVelocity(leftSpeed/3)
                        wheels[1].setVelocity(rightSpeed)
                        wheels[2].setVelocity(leftSpeed/3)
                        wheels[3].setVelocity(rightSpeed)
               # when the target in the left
                else:
                   # front left
                    if dino_x>0:
                        wheels[0].setVelocity(-leftSpeed/3)
                        wheels[1].setVelocity(rightSpeed)
                        wheels[2].setVelocity(-leftSpeed/3)
                        wheels[3].setVelocity(rightSpeed)
                   # back left
                    if dino_x<0:
                        wheels[0].setVelocity(leftSpeed/3)
                        wheels[1].setVelocity(-rightSpeed)
                        wheels[2].setVelocity(leftSpeed/3)
                        wheels[3].setVelocity(-rightSpeed)
                        
    # rotate camera 
    # 1.57=90 degree
    key=keyboard.getKey()
    if (key==ord('N')):
        print ('N is pressed')
        rotate += 0.05
        rm.setPosition(rotate)
    if (key==ord('M')):
        print ('M is pressed')
        rotate -= 0.05
        rm.setPosition(rotate)
    print('rotate '+str(rotate)) 
    if num_objects!=0: 
        rm.setPosition(rotate) 
    else:
        rotate += 0.05
        rm.setPosition(rotate)  
        
    