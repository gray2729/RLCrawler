from picrawler import Picrawler
from vilib import Vilib
import random

crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

#Move Forward
def mForward(speed):
    crawler.do_action('forward',1,speed)
    
#Move Right
def mRight(speed):
    crawler.do_action('turn right',1,speed)
    
#Move Left
def mLeft(speed):
    crawler.do_action('turn left',1,speed)
    
#Move Back
def mBack(speed):
    crawler.do_action('backward',1,speed)
    
#Test Sensors
def mTestSensor(speed):
    Vilib.color_detect("red")
    
    while Vilib.detect_obj_parameter['color_n']!=1:
        mRight(speed)
        
    print("Finished") 
    
#Random Walk
def mRandomWalk(speed):
    numActions = 0
    
    Vilib.color_detect("blue")
    while Vilib.detect_obj_parameter['color_n']!=1:
        randN = random.randint = (1, 100)
        
        if randN < 33:
            mRight(speed)
        elif randN < 66:
            mLeft(speed)
        else:
            mForward(speed)
            
        numActions += 1
            
        Vilib.color_detect("red")
        if Vilib.detect_obj_parameter['color_n']!=1:
            mBack(speed)
            
        Vilib.color_detect("blue")
    
    print("Finished Random Walk")
    return numActions

if __name__ == '__main__':
    Vilib.camera_start()
    Vilib.display()
    
    speed = 100
    
    actions = mRandomWalk(speed)
    print("Total number of actions: ", actions)
    
        
        
            