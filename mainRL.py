from RLKeras import Agent
from RLGym import RobEnv
import matplotlib.pyplot as plt
import numpy as np 
#import gymnasium as gym

def plotLearning(x, scores, epsilons, filename, lines=None):
    fig=plt.figure()
    ax=fig.add_subplot(111, label="1")
    ax2=fig.add_subplot(111, label="2", frame_on=False)

    ax.plot(x, epsilons, color="C0")
    ax.set_xlabel("Game", color="C0")
    ax.set_ylabel("Epsilon", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")

    N = len(scores)
    running_avg = np.empty(N)
    for t in range(N):
	    running_avg[t] = np.mean(scores[max(0, t-20):(t+1)])

    ax2.scatter(x, running_avg, color="C1")
    #ax2.xaxis.tick_top()
    ax2.axes.get_xaxis().set_visible(False)
    ax2.yaxis.tick_right()
    #ax2.set_xlabel('x label 2', color="C1")
    ax2.set_ylabel('Score', color="C1")
    #ax2.xaxis.set_label_position('top')
    ax2.yaxis.set_label_position('right')
    #ax2.tick_params(axis='x', colors="C1")
    ax2.tick_params(axis='y', colors="C1")

    if lines is not None:
        for line in lines:
            plt.axvline(x=line)

    plt.savefig(filename)

if __name__ == '__main__':
    #env = gym.make('LunarLander-v2', render_mode='human') #environment
    env = RobEnv()
    n_games = 500 #num of games?
    agent = Agent(alpha=0.0005, gamma=0.99, n_actions=4, epsilon=1.0, batch_size=64, input_dims=1, mem_size=100000, epsilon_end=0.01)
    #agent.load_model() #if already have a model saved
    scores = []
    eps_hist = []
    
    for i in range(n_games):
        done=False
        #truncated=False
        score=0
        observation=env.reset()
        while not done:
            #env.render()
            action = agent.choose_action(observation)
            observation_new, reward, done, info = env.step(action)
            score += reward
            agent.remember(observation, action, reward, observation_new, done)
            observation = observation_new
            agent.learn()
        
        eps_hist.append(agent.epsilon)
        scores.append(score)
        
        avg_score = np.mean(scores[max(0, i-100):(i+1)]) #average of every 100 games
        print('episode', i, 'score %.2f' % score, 'average score %.2f' % avg_score)
        
        if i % 10 == 0 and i > 0: #save model every 10 games
            agent.save_model()
    
    filename = 'testRL.png'
    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_hist, filename)
    
    