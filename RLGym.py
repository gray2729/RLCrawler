from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import random

class RobEnv(Env):
    def __init__(self):
        self.action_space = Discrete(3)
        self.state = float(str(random.randint(0, 5))+'.'+str(random.randint(0, 5)))
        
        dictState = {}
        
        dictState[0.0]=[0.1,1.0,0.0,0.0]
        dictState[0.1]=[0.2,0.1,0.0,0.1]
        dictState[0.2]=[0.3,1.2,0.1,0.2]
        dictState[0.3]=[0.4,0.3,0.2,0.3]
        dictState[0.4]=[0.5,1.4,0.3,0.4]
        dictState[0.5]=[0.5,1.5,0.4,0.5]
        dictState[1.0]=[1.0,2.0,1.0,0.0]
        dictState[1.2]=[1.2,2.2,1.2,0.2]
        dictState[1.4]=[1.5,2.4,1.4,0.4]
        dictState[1.5]=[1.5,2.5,1.4,0.5]
        dictState[2.0]=[2.1,3.0,2.0,1.0]
        dictState[2.1]=[2.2,2.1,2.0,2.1]
        dictState[2.2]=[2.3,3.2,2.1,1.2]
        dictState[2.3]=[2.4,2.3,2.2,2.3]
        dictState[2.4]=[2.5,3.4,2.3,1.4]
        dictState[2.5]=[2.5,3.5,2.4,1.5]
        dictState[3.0]=[3.0,4.0,3.0,2.0]
        dictState[3.2]=[3.2,4.2,3.2,2.2]
        dictState[3.4]=[3.5,4.4,3.4,2.4]
        dictState[3.5]=[3.5,3.5,3.5,3.5]
        dictState[4.0]=[4.1,5.0,4.0,3.0]
        dictState[4.1]=[4.2,5.1,4.0,4.1]
        dictState[4.2]=[4.3,5.2,4.1,3.2]
        dictState[4.3]=[4.4,5.3,4.2,4.3]
        dictState[4.4]=[4.5,5.4,4.3,3.4]
        dictState[4.5]=[4.5,5.5,4.4,3.5]
        dictState[5.0]=[5.1,5.0,5.0,4.0]
        dictState[5.1]=[5.2,5.1,5.0,4.1]
        dictState[5.2]=[5.3,5.2,5.1,4.2]
        dictState[5.3]=[5.4,5.3,5.2,4.3]
        dictState[5.4]=[5.5,5.4,5.3,4.4]
        dictState[5.5]=[5.5,5.5,5.4,4.5]
        
        self.states = dictState
        
    def step(self, action):
        self.state = self.states[self.state][action]
        
        if self.state == 3.5:
            reward = 0
            done = True
        else:
            reward = -1
            done = False
        
        info = {}
        return self.state, reward, done, info
        
    def render(self):
        pass
    
    def reset(self):
        self.state = float(str(random.randint(0, 5))+'.'+str(random.randint(0, 5)))
        while self.state in {1.1, 1.3, 3.1, 3.3, 3.5}:
            self.state = float(str(random.randint(0, 5))+'.'+str(random.randint(0, 5)))
            
        return self.state