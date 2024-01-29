from picrawler import Picrawler
from vilib import Vilib
import random
from time import sleep

crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

#Move Forward
def mForward(speed):
    crawler.do_action('forward',3,speed)
    
#Move Right
def mRight(speed):
    crawler.do_action('turn right',3,speed)
    crawler.do_action('forward', 3,speed)
    crawler.do_action('turn left', 3,speed)
    
#Move Left
def mLeft(speed):
    crawler.do_action('turn left', 3,speed)
    crawler.do_action('forward', 3,speed)
    crawler.do_action('turn right',3,speed)
    
#Move Back
def mBack(speed):
    crawler.do_action('backward',3,speed)
    
if __name__ == '__main__':
    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect("green")
    
    speed = 100
    
    while Vilib.detect_obj_parameter['color_n']!=1:
        randN = random.randint(1, 100)
    
        if randN < 30:
            mForward(speed)
            
        elif randN < 50:
            mRight(speed)
            
        elif randN < 70:
            mLeft(speed)
            
        else:
            mBack(speed)
        
        
            