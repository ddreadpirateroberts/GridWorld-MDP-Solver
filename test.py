import pygame 
from gridworld import Gridworld, DisplayMode
from optimal_policy import ValueIteration, PolicyIteration
import time 
from random import randint


class Test: 
    def __init__(self):
        self.model = Gridworld(70, 70, random=True, wall_ratio=25)
        print("GridWorld has been constructed")
        
    def extract_policy(self): 
        pi = {(i, j): 1 for i in range(self.model.rows)
                        for j in range(self.model.cols)}
        policy_iter = PolicyIteration(self.model, pi)
        policy_iter(display_result=False)
        pi = dict()
        for coor, state in self.model.grid.items():
            pi[coor] = state.dir 
        return pi 
    
    def runtime(self, n=3): 
        res = {"Value": 0, "Policy": 0}
        value_iter = ValueIteration(self.model)     
        pi = {(i, j): 1 for i in range(self.model.rows)
                        for j in range(self.model.cols)}
        policy_iter = PolicyIteration(self.model, pi) 

        print("Initiating runtime test...")
        for i in range(n):    
            self.model.wipe()    
            start = time.time()               
            value_iter(display_result=False, theta=0.0001)
            res["Value"] += time.time() - start
            
            self.model.wipe()
            policy_iter._load_policy(pi)
            start = time.time()
            policy_iter(display_result=False, theta=0.0001)
            res["Policy"] += time.time() - start
            
        res = {i: j/n for i, j in res.items()}
        print("average:", res)
        
    def robot_runner(self, state, pi): 
        reward, steps, current_state = 0, 0, state
        commit = self.model.commit
        while True:
            steps += 1
            if current_state.is_pit() or current_state.is_diamond():
                break
            
            action = pi[current_state.get_state_coor()]
            rand = randint(1, 100)
            if rand <= (1 - self.model.noise) * 100: 
                current_state = commit(current_state, action)
            elif (1 - self.model.noise) * 100 < rand <= (1 - self.model.noise/2) * 100: 
                current_state = commit(current_state, (action-1)%4)
            else: 
                current_state = commit(current_state, (action+1)%4)
            
            reward += self.model.living_reward
            
        return reward + self.model.discount ** (steps - 1) * current_state.util 

    def robot(self, k=1000): 
        self.optimal_policy = self.extract_policy()
        state = self.model.get_random_tile()
        total_reward = 0 
        for _ in range(k): 
            total_reward += self.robot_runner(state, self.optimal_policy)
        total_reward /= k 
        print(f"({state.row}, {state.col}):", total_reward)
    
                    
test = Test()
test.runtime()

# test.robot()


test.model.display(DisplayMode.UTILxDIR)
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w: 
                test.model.wipe()
                test.model.display(DisplayMode.UTILxDIR)
    
    pressed = pygame.key.get_pressed()
        
    if pressed[pygame.K_v]: 
        test.model.wipe()
        value_iter = ValueIteration(test.model)
        if pressed[pygame.K_1]: 
            value_iter(display_mode=DisplayMode.UTILxDIR)
        elif pressed[pygame.K_2]:
            value_iter(display_mode=DisplayMode.QVAL)

    if pressed[pygame.K_p]: 
        test.model.wipe()
        pi = {(i, j): 1 for i in range(test.model.rows)
                            for j in range(test.model.cols)}
        policy_iter = PolicyIteration(test.model, pi)
        
        if pressed[pygame.K_1]: 
            policy_iter(display_mode=DisplayMode.UTILxDIR)
        elif pressed[pygame.K_2]:
            policy_iter(display_mode=DisplayMode.QVAL)
