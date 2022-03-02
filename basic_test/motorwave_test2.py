from motor.MotorDriver import MotorDriver
import time
    
Motor = MotorDriver()
print("PCA9685 MotorDriver")

try:
    while 1:
        # control 2 motor
        Motor.MotorRun(0, 'forward', 0.5)
        Motor.MotorRun(1, 'forward', 0.5)

        time.sleep(1);

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("\r\nctrl + c:")
    Motor.AllMotorStop()
    exit()


