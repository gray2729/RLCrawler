from RLGym import RobEnv
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#Parameters
seed = 32
gamma = 0.99 #Discount reward from past
epsilon = 1.0 #epsilon greedy parameter
epsilon_min = 0.1 
epsilon_max = 1.0
epsilon_interval = epsilon_max - epsilon_min #epsilon reduction rate
batch_size = 5
max_episode_step = 300

num_actions = 3

def create_qmodel():
    inputs = layers.Input(shape=(2, ))
    #layer1 = layers.Conv2D(256, strides=4, activation="relu")(inputs)
    #layer2 = layers.Conv2D(256, strides=2, activation="relu")(layer1)
    #layer3 = layers.Conv2D(256, strides=1, activation="relu")(layer2)

    #layer4 = layers.Flatten()(layer3)

    layer1 = layers.Dense(256, activation="relu")(inputs)
    layer2 = layers.Dense(256, activation="relu")(layer1)
    action = layers.Dense(num_actions, activation="linear")(layer2)

    return keras.Model(inputs=inputs, outputs=action)

model = create_qmodel()
model_target = create_qmodel()

optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)

action_history = []
state_history = []
state_next_history = []
reward_history = []
done_history = []
episode_reward_history = []
running_reward = 0
episode_count = 0

explore_frame_count = 0
epsilon_random_frames = 3000 #number of frames for exploration
epsilon_greedy_frames = 1000.0

max_memory_length = 1000
update_after_action = 3 #updates model after 3 actions
update_target_model = 1000 # how often to update model

loss_function = keras.losses.Huber() 

env = RobEnv()
n_games = 500
scores = []
eps_hist = []

keras.utils.disable_interactive_logging()

for i in range(n_games):
    done=False
    score = 0
    timestep = 0
    
    state=env.reset()
    
    while done==False and timestep<max_episode_step:
        explore_frame_count+=1
        if explore_frame_count<epsilon_random_frames or epsilon>np.random.rand(1)[0]:
            action = np.random.choice(num_actions) #take random action, exploring
        else:
            state_tensor = tf.convert_to_tensor(state)
            state_tensor = tf.expand_dims(state_tensor, 0)
            action_probs = model(state_tensor, training=False) #predict action values
                        
            action = tf.argmax(action_probs[0]).numpy() #take best action
        
        epsilon -= epsilon_interval/epsilon_greedy_frames #epsilon decay
        epsilon = max(epsilon, epsilon_min) 
        
        state_next, reward, done = env.step(action) #take step
        
        score += reward
        
        action_history.append(action)
        state_history.append(state)
        state_next_history.append(state_next)
        reward_history.append(reward)
        state = state_next
        
        if explore_frame_count % update_after_action == 0 and len(reward_history)>batch_size:
            indices = np.random.choice(range(len(reward_history)), size=batch_size)
            
            state_sample = np.array([state_history[i] for i in indices])
            state_next_sample = np.array([state_next_history[i] for i in indices])
            rewards_sample = np.array([reward_history[i] for i in indices])
            action_sample = np.array([action_history[i] for i in indices])
        
            future_rewards = model_target.predict(state_next_sample)
            updated_qvalues = rewards_sample + gamma * tf.reduce_max(future_rewards, axis=1)
            
            masks = tf.one_hot(action_sample, num_actions)
            
            with tf.GradientTape() as tape:
                q_values = model(state_sample)
                q_actions = tf.reduce_sum(tf.multiply(q_values, masks), axis=1)
                loss = loss_function(updated_qvalues, q_actions)
                
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))
            
        if explore_frame_count % update_target_model == 0:
            model_target.set_weights(model.get_weights())
            
        if len(reward_history) > max_memory_length:
            del reward_history[:1]
            del state_history[:1]
            del state_next_history[:1]
            del action_history[:1]
            del done_history[:1]
            
    scores.append(score)
    
    avg_score = np.mean(scores[max(0, i-100):(i+1)]) #average of every 100 games
    print('episode', i, 'score %.2f' % score, 'average score %.2f' % avg_score)