from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np

class ReplayBuffer(object):
    def __init__(self, max_size, input_shape, n_actions, discrete=False):
        self.mem_size = max_size #max size of memory
        self.mem_cntr = 0
        self.discrete = discrete #discrete action space or not, determines how to store actions
        self.state_memory = np.zeros((self.mem_size, input_shape)) #takes states from environment and stores them
        self.new_state_memory = np.zeros((self.mem_size, input_shape)) #keeps track of new states after action
        dtype2 = np.int8 if self.discrete else np.float32 #if discrete, saves as int
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=dtype2)
        self.reward_memory = np.zeros(self.mem_size) #keeps track of rewards agent recieves
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.float32) #keeps track of terminal flags, doesn't last reward
        
    def store_transition(self, state, action, reward, state_new, done):
        #storing the state-action-reward-new_state-done flags in memory
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_new
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done) 
        if self.discrete:
            actions = np.zeros(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions
        else:
            self.action_memory[index] = action
        self.mem_cntr += 1
    
    def sample_buffer(self, batch_size):
        #samples subset of memory
        max_mem = min(self.mem_cntr, self.mem_size) #maximum memory written to
        batch = np.random.choice(max_mem, batch_size) 
        
        states = self.state_memory[batch]
        states_new = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]
        
        return states, actions, rewards, states_new, terminal
    
def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims): 
    #lr: learning rate, 
    #fc1_dims: first fully connected layer dim, 
    #fc2_dims: second fully connected layer dim
    model = Sequential([
            Dense(fc1_dims, input_shape=(input_dims, )),
            Activation('relu'),
            Dense(fc2_dims),
            Activation('relu'),
            Dense(n_actions)
        ])
    model.compile(optimizer=Adam(lr=lr), loss='mse')
    
    return model

class Agent(object):
    def __init__(self, alpha, gamma, n_actions, epsilon, batch_size, input_dims, epsilon_dec=0.996, epsilon_end=0.01, mem_size=1000000, fname='dqn_model.h5'):
        #alpha: learning rate
        #gamma: discount factor, discounts future rewards
        #epsilon: less than eps take random action, else greedy action
        #epsilon_dec: decreases over time
        #epsilon_end: minimum epsilon
        self.action_space = [i for i in range(n_actions)] #used to select random action
        self.n_action = n_actions
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_dec = epsilon_dec
        self.epsilon_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        
        self.memory = ReplayBuffer(mem_size, input_dims, n_actions, discrete=True)
        self.q_eval = build_dqn(alpha, n_actions, input_dims, 256, 256)
        
    def remember(self, state, action, reward, new_state, done):
        #interfacing with memory to save state transition
        self.memory.store_transition(state, action, reward, new_state, done)
        
    def choose_action(self, state):
        state = np.expand_dims(state, axis=0)
        rand = np.random.random()
        if rand < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            actions = self.q_eval.predict(state, verbose=0) #get state, actions for state
            action = np.argmax(actions) #select maximum value for action
        
        return action 
    
    def learn(self):
        #temperal difference learning method: learns on every step
        if self.memory.mem_cntr < self.batch_size:
            #fill up batch size of memory
            return
        state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)
        action_values = np.array(self.action_space, dtype=np.int8)
        action_indices = np.dot(action, action_values) #indice of action taken, int (1, 2, 3, etc)

        q_eval = self.q_eval.predict(state, verbose=0) #current state
        q_next = self.q_eval.predict(new_state, verbose=0) #next state
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        q_target[batch_index, action_indices] = reward + self.gamma*np.max(q_next, axis=1)*done 
        #np.max is maximum action for next state

        _ = self.q_eval.fit(state, q_target, verbose=0) #verbose suppresses the output, 
        
        self.epsilon = self.epsilon*self.epsilon_dec if self.epsilon > self.epsilon_min else self.epsilon_min
    
    def save_model(self):
        self.q_eval.save(self.model_file)
    
    def load_model(self):
        self.q_eval = load_model(self.model_file)
        