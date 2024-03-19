from gymnasium import Env
from gymnasium import spaces
import numpy as np
#import random

class RobEnv(Env):
    def __init__(self):
        self.size = 5
        self.action_space = spaces.Discrete(3)
        
        self.observation_space = spaces.Dict(
            {"agent": spaces.Box(0, self.size-1, shape=(2,), dtype=int)}
        )
        
        self.movements_actions = {
            0: np.array([0, 1]), #move forward
            1: np.array([1, 0]), #move left
            2: np.array([-1, 0]) # move right
        }
        
    def step(self, action):
        movement = self.movements_actions[action]
        
        self.current_state = np.clip(self.current_state + movement, 0, self.size-1)
        if np.array_equal(self.current_state, np.array([4,4])):
            reward = 0
            done = True
        else:
            reward = -1
            done = False
        observation = self.current_state
        
        return observation, reward, done
        
    def render(self):
        pass
    
    def reset(self):
        self.current_state = np.array([0,0])
        observation = self.current_state
            
        return observation