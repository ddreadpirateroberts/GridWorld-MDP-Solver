from gridworld import Tile, Gridworld, DisplayMode
import pygame as pg


class MDPSolver:
    def __init__(self, model: Gridworld):
        self.model = model
        self.clock = pg.time.Clock()
        
    def get_states(self):
        return self.model.grid.values()
    
    def decode_policy(self, pi):
        for key, value in pi.items():
            pi[key] = self.decode(value)
        return pi

    def decode(self, dir):
        if dir in ["L", 0]: 
            return 0 
        elif dir in ["U", 1]: 
            return 1
        elif dir in ["R", 2]: 
            return 2 
        elif dir in ["D", 3]: 
            return 3 
        
    def arg_max(self, state):
        arg, max = None, -float('inf')
        for dir, value in state.aval.items():
            if value > max:
                arg = dir
                max = value
        return arg, max

    def estimate_util(self, state, action): 
        mdl = self.model
        reward, gamma, noise, commit = mdl.living_reward, mdl.discount, mdl.noise, mdl.commit
        expu = (1-noise) * (reward + gamma * commit(state, action).util)
        expu += (noise/2) * (reward + gamma * commit(state, (action-1)%4).util)
        expu += (noise/2) * (reward + gamma * commit(state, (action+1)%4).util)
        return expu


class ValueIteration(MDPSolver):
    def __init__(self, model: Gridworld) -> None:
        super().__init__(model)

    def eval_qstar(self, state: Tile, action: int):
        exp_u = self.estimate_util(state, action)
        state.set_aval(action, exp_u)

    def __call__(self, theta=0.0001, display_result=True, display_mode=DisplayMode.QVAL):
        while True:            
            for state in self.get_states():
                if state.is_walkable():
                    for action in range(4):
                        self.eval_qstar(state, action)

            delta = 0
            for state in self.get_states():
                if state.is_walkable():
                    dir, new_util = self.arg_max(state)
                    delta = max(delta, abs(state.util - new_util))
                    state.util = new_util
                    state.dir = dir
                    
            if display_result: 
                self.clock.tick(4)
                self.model.display(display_mode)
                
            if delta < theta:
                break


class PolicyIteration(MDPSolver):
    def __init__(self, model: Gridworld, pi: set) -> None:
        super().__init__(model)
        self._load_policy(pi)

    def _load_policy(self, pi: dict): 
        pi = self.decode_policy(pi)
        for coor, dir in pi.items(): 
            self.model.grid[coor].dir = dir
            
    def eval_upi(self, state: Tile) -> float:            
        return self.estimate_util(state, state.dir)
    
    def policy_evaluation(self, theta, max_iter, display_result, display_mode):
        for _ in range(max_iter):
            delta = 0
            for state in self.get_states():
                if state.is_walkable():
                    new_util = self.eval_upi(state)
                    delta = max(delta, abs(state.util - new_util))
                    state.util = new_util
                    
            if display_result: 
                self.clock.tick(8)
                self.model.display(display_mode)
                
            if delta < theta:
                break
        
    def policy_improvement(self):
        unchanged = True
        for state in self.get_states():
            if state.is_walkable():
                for action in range(4):
                    expu = self.estimate_util(state, action)
                    state.set_aval(action, expu)
                best_action, meu = self.arg_max(state)

                piutil = state.aval[state.dir]
                if best_action != state.dir and meu != piutil:
                    state.dir = best_action
                    unchanged = False
        return unchanged

    def __call__(self, theta=0.0001, display_result=True, display_mode=DisplayMode.QVAL, max_iter=15):
        for _ in range(max_iter):
            self.policy_evaluation(theta, max_iter, display_result, display_mode)
            unchanged = self.policy_improvement()
            
            if display_result: 
                self.clock.tick(3)
                self.model.display(display_mode)
                
            if unchanged:
                break
            

if __name__ == "__main__":
    grid = Gridworld(6, 6, True)                    
    grid.display(DisplayMode.UTILxDIR)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

                if event.key == pg.K_w: 
                    grid.wipe()
                    grid.display(DisplayMode.UTILxDIR)
                
                if event.key == pg.K_n: 
                    grid = Gridworld(6, 6, True)
                    grid.display(DisplayMode.UTILxDIR)
                    
        pressed = pg.key.get_pressed()
        
        if pressed[pg.K_v]: 
            grid.wipe()
            value_iter = ValueIteration(grid)
            if pressed[pg.K_1]: 
                value_iter(display_mode=DisplayMode.UTILxDIR)
            elif pressed[pg.K_2]:
                value_iter(display_mode=DisplayMode.QVAL)

        if pressed[pg.K_p]: 
            grid.wipe()
            pi = {(i, j): "U" for i in range(grid.rows)
                                for j in range(grid.cols)}
            policy_iter = PolicyIteration(grid, pi)
            
            if pressed[pg.K_1]: 
                policy_iter(display_mode=DisplayMode.UTILxDIR)
            elif pressed[pg.K_2]:
                policy_iter(display_mode=DisplayMode.QVAL)
