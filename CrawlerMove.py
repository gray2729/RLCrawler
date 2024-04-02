from picrawler import Picrawler
from vilib import Vilib
import random
from time import sleep
import time

crawler = Picrawler([10,11,12,4,5,6,1,2,3,7,8,9])

#Move Forward
def mForward(speed):
    Vilib.color_detect("red")
    sleep(0.2)
    if Vilib.detect_obj_parameter['color_n']>=1:
        crawler.do_action('forward',4,speed)
    
#Turn Right
def mRight(speed):
    crawler.do_action('turn left angle',9,speed) #10
    
#Turn Left
def mLeft(speed):
    crawler.do_action('turn right angle',9,speed) #10
    
#Move Right
def mSRight(speed):
    mRight(speed)
    mForward(speed)
    mLeft(speed)

#Move Left
def mSLeft(speed):
    mLeft(speed)
    mForward(speed)
    mRight(speed)
    
#Move Back
def mBack(speed):
    crawler.do_action('backward',4,speed)
    
#Movement Model Walk
def mMModelWalk(actions, speed):
    Vilib.camera_start()
    Vilib.display()
    
    score = 0
    startTime = time.time()
    
    for i in range(len(actions)):
        if actions[i] == 0:
            mForward(speed)
        elif actions[i] == 1:
            mSLeft(speed)
        else:
            mSRight(speed)
            
        score -= 1
        
        sleep(0.2)
        
    intervalTime = time.time()-startTime
    
    return intervalTime, score

#Read Learning Movement
def ReadActions(fileName):
    WalkFile = open(fileName, "r")
    
    actions = []
    
    for line in WalkFile:
        actions.append([int(i) for i in line.split()])
        
    return actions
    
      
#Random Walk
def mRandomMWalk(speed):
    Vilib.camera_start()
    Vilib.display()
    
    WalkFile = open("RandomMWalk.txt", "a")
    
    score = 0
    startTime = time.time()
    
    Vilib.color_detect("blue")
    while Vilib.detect_obj_parameter['color_n']<1:
        randN = random.randint = (1, 100)
        
        if randN < 15:
            mSRight(speed)
        elif randN < 30:
            mSLeft(speed)
        else:
            mForward(speed)
            
        score -= 1
            
        Vilib.color_detect("blue")
        sleep(0.2)
        
    intervalTime = time.time()-startTime
    
    print("Finished Random Walk")
    print("Score: ", score)
    print("Length of time: ", intervalTime)
    
    WalkFile.write(str(score)+ " " +str(intervalTime))
    WalkFile.close()
    

if __name__ == '__main__':
    speed = 100

#Random Walk    
    #mRandomMWalk(speed)
   
#Movement Model Learning Response
    actions = ReadActions("LearningActions.txt")
    mTime, score=mMModelWalk(actions[0], speed)
    
    print(mTime)
    print(score)
        