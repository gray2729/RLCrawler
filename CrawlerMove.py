from picrawler import Picrawler
import random
#from time import sleep

crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

#Move Forward
def mForward(speed):
    crawler.do_action('forward',2,speed)
    
#Move Right
def mRight(speed):
    crawler.do_action('turn right',2,speed)
    
#Move Left
def mLeft(speed):
    crawler.do_action('turn left',2,speed)
    
#Move Back
def mBack(speed):
    crawler.do_action('backward',2,speed)
    
#Turn Right
def mTRight(speed):
    crawler.do_action('turn right angle',2,speed)
    
#Turn Left
def mTLeft(speed):
    crawler.do_action('turn left angle',2,speed)