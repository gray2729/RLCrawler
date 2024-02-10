from picrawler import Picrawler
from vilib import Vilib
from robot_hat import Music, TTS
import random

crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

#Move Forward
def mForward(speed):
    crawler.do_action('forward',3,speed)
    
#Move Right
def mRight(speed):
    crawler.do_action('turn right',3,speed)
    
#Move Left
def mLeft(speed):
    crawler.do_action('turn left', 3,speed)
    
#Move Back
def mBack(speed):
    crawler.do_action('backward',3,speed)
    
#Test Sensors
def mTestSensor(speed):
    Vilib.color_detect("red")
    
    while Vilib.detect_obj_parameter['color_n']!=1:
        mRight(speed)
        
    Music.sound_effect_play('./sounds/sign.wav')
        
    

if __name__ == '__main__':
    Vilib.camera_start()
    Vilib.display()
    
    Music.music_set_volume(20)
    TTS.lang("en-US")
    
    speed = 100
    
    mTestSensor(speed)
    
    #while Vilib.detect_obj_parameter['color_n']!=1:
     #   randN = random.randint(1, 100)
    
     #   if randN < 30:
     #       mForward(speed)
            
     #   elif randN < 50:
     #       mRight(speed)
            
     #   elif randN < 70:
     #       mLeft(speed)
            
     #   else:
     #       mBack(speed)
        
        
            