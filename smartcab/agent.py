import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.c_actions = [None,'forward','left','right']
        self.c_light = ['red','green']
        self.q_values_table = {}
        for i in range(len(self.c_actions)):
            for j in range(len(self.c_light)):
                for k in range(len(self.c_actions)):
                    for l in range(len(self.c_actions)):
                        for m in range(len(self.c_actions)):
                            self.q_values_table[self.c_actions[i],self.c_light[j],self.c_actions[k],self.c_actions[l],self.c_actions[m]] = {None : 0, 'forward': 0, 'left' : 0, 'right': 0} 
        self.epsilon = 0.1
        self.discount = 0.8
        self.learning_rate = 0.3
        self.total_reward = 0

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.total_reward = 0
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        
        # TODO: Update state
        self.state = (inputs['oncoming'], inputs['light'], self.next_waypoint, inputs['right'], inputs['left'])                 
        
        # TODO: Select action according to your policy
        
        if random.random() > self.epsilon:
           self.temp_action = max(self.q_values_table[self.state].values())
           for i,j in self.q_values_table[self.state].iteritems():
               if j == self.temp_action:
    	          action = i  
        else:
             action = random.choice(self.env.valid_actions) 
        
        # Question 1 - action = random.choice(self.env.valid_actions)
        
        # Execute action and get reward
        reward = self.env.act(self, action)
        
        self.total_reward += reward  
        # TODO: Learn policy based on state, action, reward
        self.q_values_table[self.state][action] = self.q_values_table[self.state][action] + self.learning_rate*(reward + self.discount*(max(self.q_values_table[self.next_state(t)].values()))) - self.q_values_table[self.state][action]       
        
        if self.next_waypoint == None:
           print "Destination reached"
        elif deadline == 0: 
             print "Smart cab failed"   

        
        
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}, total_reward = {}".format(deadline, inputs, action, reward, self.total_reward)  # [debug]
    def next_state(self, t):
        self.new_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs_new = self.env.sense(self)
        self.state_new = (inputs_new['oncoming'], inputs_new['light'], self.new_waypoint, inputs_new['right'], inputs_new['left'])
        return self.state_new

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.3, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
