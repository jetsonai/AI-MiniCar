
from motor.MotorDriver import MotorDriver
import time

try:
    Motor = MotorDriver()
    # control 2 motor
    Motor.MotorRun(0, 'forward', 0.3)
    Motor.MotorRun(1, 'forward', 0.3)
    print("PCA9685 MotorDriver")
    time.sleep(3);
    Motor.AllMotorStop()

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("\r\nctrl + c:")
    Motor.AllMotorStop()
    exit()

